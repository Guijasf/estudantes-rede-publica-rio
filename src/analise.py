"""Calcula as comparações do estudo e exporta as figuras do artigo."""

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import pandas as pd

from .etl import ANOS, ROOT, carregar_tabela, salvar_tabela


PENHA_E_VIGARIO_GERAL = ("XI", "XXXI")
COMPARAVEIS_MUNICIPIO = [
    "Total", "Creche", "Pré-escola", "Classe de alfabetização",
    "Alfabetização de adultos", "Ensino fundamental", "Ensino médio",
    "Graduação", "Mestrado e doutorado",
]
PALETA = {"aumento": "#127069", "queda": "#a84435", "texto": "#18283f"}


def agregar_niveis(dados):
    chaves = ["ano", "escopo", "ra_codigo", "territorio", "nivel_ensino"]
    return (
        dados.groupby(chaves, sort=False, dropna=False)["estudantes_estimados"]
        .agg(lambda valores: valores.sum(min_count=len(valores)))
        .reset_index()
    )


def variacoes(tabela):
    antes, depois = ANOS
    tabela = tabela.loc[:, [antes, depois]].copy()
    tabela["diferenca"] = tabela[depois] - tabela[antes]
    tabela["variacao_pct"] = tabela["diferenca"].div(tabela[antes].where(tabela[antes] > 0)) * 100
    return tabela


def comparar_municipio(niveis):
    municipio = niveis.loc[niveis["escopo"] == "municipio"]
    tabela = municipio.pivot(
        index="nivel_ensino", columns="ano", values="estudantes_estimados",
    )
    return variacoes(tabela.loc[COMPARAVEIS_MUNICIPIO])


def comparar_regioes(niveis, nivel):
    regioes = niveis.loc[
        (niveis["escopo"] == "regiao") & (niveis["nivel_ensino"] == nivel)
        & ~niveis["ra_codigo"].isin(PENHA_E_VIGARIO_GERAL)
    ]
    tabela = regioes.pivot(
        index=["ra_codigo", "territorio"], columns="ano", values="estudantes_estimados",
    )
    return variacoes(tabela.dropna(subset=list(ANOS))).sort_values("diferenca", ascending=False)


def diagnosticar_cobertura(dados):
    totais = dados.loc[dados["nivel_ensino"] == "Total"]
    regioes = totais.loc[totais["escopo"] == "regiao"].groupby("ano")
    municipio = totais.loc[totais["escopo"] == "municipio"].set_index("ano")
    return pd.DataFrame({
        "regioes_publicadas": regioes.size(),
        "soma_regioes": regioes["estudantes_estimados"].sum(),
        "total_municipal": municipio["estudantes_estimados"],
    }).assign(diferenca=lambda tabela: tabela["soma_regioes"] - tabela["total_municipal"])


def sensibilidade_penha(niveis):
    recorte = niveis.loc[
        (niveis["escopo"] == "regiao") & niveis["ra_codigo"].isin(PENHA_E_VIGARIO_GERAL)
        & niveis["nivel_ensino"].isin(["Total", "Creche"])
    ]
    valores = recorte.groupby(["nivel_ensino", "ano"])["estudantes_estimados"].sum().unstack()
    return variacoes(valores.loc[["Total", "Creche"]])


def numero_br(valor, decimais=0, sinal=False):
    formato = f"{'+' if sinal else ''},.{decimais}f"
    return format(valor, formato).translate(str.maketrans(",.-", ".,−"))


def grafico_variacao(valores, unidade="mil estudantes estimados"):
    """Usa origem zero e rótulos com sinal para distinguir altas e quedas."""
    grafico, eixo = plt.subplots(
        figsize=(8.2, 0.38 * len(valores) + 1.0), layout="constrained",
    )
    valores = valores.sort_values()
    cores = [PALETA["aumento"] if valor >= 0 else PALETA["queda"] for valor in valores]
    barras = eixo.barh(valores.index, valores, color=cores, height=0.62)
    eixo.axvline(0, color="#677789", linewidth=0.8)
    eixo.bar_label(
        barras, labels=[numero_br(valor, sinal=True) for valor in valores],
        color=PALETA["texto"], padding=5, fontsize=9,
    )
    eixo.margins(x=0.18)
    eixo.set_xlabel(f"Variação de 2000 a 2010 ({unidade})", labelpad=8, color=PALETA["texto"])
    eixo.xaxis.set_major_locator(MaxNLocator(nbins=6))
    eixo.xaxis.set_major_formatter(FuncFormatter(lambda valor, _: numero_br(valor / 1000, 1).removesuffix(",0")))
    eixo.grid(axis="x", color="#dce3ec", linewidth=0.7)
    eixo.set_axisbelow(True)
    eixo.tick_params(axis="both", colors=PALETA["texto"], length=0, labelsize=9)
    for borda in eixo.spines.values():
        borda.set_visible(False)
    return grafico


def maiores_variacoes(regioes, quantidade=4):
    diferencas = regioes["diferenca"]
    return pd.concat([
        diferencas.loc[diferencas > 0].head(quantidade),
        diferencas.loc[diferencas < 0].tail(quantidade),
    ]).droplevel("ra_codigo")


def exportar_figuras(niveis, destino=ROOT / "docs" / "assets"):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    municipio = comparar_municipio(niveis).drop(index="Total")
    regioes = comparar_regioes(niveis, "Total")
    creche = comparar_regioes(niveis, "Creche")
    series = {
        "variacao-niveis.png": municipio["diferenca"],
        "variacao-regioes.png": maiores_variacoes(regioes),
        "variacao-creche.png": creche["diferenca"].head(7).droplevel("ra_codigo"),
    }
    for nome, valores in series.items():
        figura = grafico_variacao(valores)
        figura.savefig(destino / nome, dpi=210, facecolor="white")
        plt.close(figura)
    return list(series)


def exportar_dados_regioes(niveis, destino=ROOT / "docs" / "assets"):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    indicadores = {}
    for nivel in ("Total", "Creche"):
        tabela = comparar_regioes(niveis, nivel).reset_index()
        indicadores[nivel] = json.loads(tabela.to_json(
            orient="records", force_ascii=False, double_precision=12,
        ))
    arquivo = destino / "comparacoes-regionais.js"
    arquivo.write_text(
        "const DADOS_REGIONAIS = " + json.dumps(indicadores, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    return arquivo


def main():
    dados = carregar_tabela()
    salvar_tabela(dados)
    niveis = agregar_niveis(dados)
    arquivos = exportar_figuras(niveis)
    exportar_dados_regioes(niveis)
    print("Figuras exportadas em docs/assets: " + ", ".join(arquivos))


if __name__ == "__main__":
    main()
