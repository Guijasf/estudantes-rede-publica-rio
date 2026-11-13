"""Converte a planilha original em uma tabela longa com rastreabilidade."""

from argparse import ArgumentParser
from math import isfinite
from numbers import Real
from pathlib import Path
import re
from tempfile import NamedTemporaryFile

import pandas as pd
from xlrd import colname


ROOT = Path(__file__).resolve().parents[1]
ARQUIVO_BRUTO = ROOT / "data" / "raw" / "tabela_892.xls"
ARQUIVO_TRATADO = ROOT / "data" / "processed" / "estudantes.csv.gz"
ANOS = (2000, 2010)
QUANTIDADE_COLUNAS = {2000: 16, 2010: 15}
PADRAO_RA = re.compile(r"([IVX]+) (.+)")

NIVEIS_DA_FONTE = {
    "Creche": "Creche",
    "Pré-escola": "Pré-escola",
    "Classe de alfabetização": "Classe de alfabetização",
    "Alfabetização de adultos": "Alfabetização de adultos",
    "Ensino fundamental ou 1o. Grau": "Ensino fundamental",
    "Ensino fundamental ou 1º Grau": "Ensino fundamental",
    "Ensino médio ou 2o. Grau": "Ensino médio",
    "Ensino médio ou 2º Grau": "Ensino médio",
    "Pré-vestibular": "Pré-vestibular",
    "Ensino superior- Graduação": "Graduação",
    "Ensino superior - Graduação": "Graduação",
    "Especialização de nível Superior": "Especialização",
    "Mestrado ou Doutorado": "Mestrado e doutorado",
    "Mestrado": "Mestrado e doutorado",
    "Doutorado": "Mestrado e doutorado",
}
MODALIDADES_DA_FONTE = {
    "Regular seriado": "Regular seriado",
    "Regular não seriado": "Regular não seriado",
    "Regular": "Regular",
    "Supletivo": "Supletivo",
}
NOMES_REGIONAIS = {
    "IIha do Governador": "Ilha do Governador",
    "SantaTeresa": "Santa Teresa",
}


def texto(valor):
    """Retira espaços excedentes, inclusive os não separáveis."""
    return " ".join(str(valor).split())


def interpretar_valor(valor, ano):
    """Mantém a distinção indicada nas notas de rodapé da planilha."""
    if isinstance(valor, Real) and not isinstance(valor, bool):
        if isfinite(valor) and valor >= 0:
            return float(valor), "informado"
    if ano == 2000 and valor == "...":
        return None, "indisponivel"
    if ano == 2010 and valor == "-":
        return 0.0, "zero_explicito"
    raise ValueError(f"Valor fora do padrão na aba {ano}: {valor!r}")


def colunas_dos_indicadores(planilha, ano):
    """Lê os níveis e modalidades a partir do cabeçalho mesclado."""
    limite = QUANTIDADE_COLUNAS[ano]
    if planilha.shape[1] < limite or texto(planilha.iat[4, 2]) != "Total":
        raise ValueError(f"Cabeçalho inesperado na aba {ano}.")

    colunas = [(2, "Total", "Total publicado")]
    nivel_original = ""
    for coluna in range(3, limite):
        nivel_original = texto(planilha.iat[5, coluna]) or nivel_original
        nivel = NIVEIS_DA_FONTE[nivel_original]
        subcategoria = texto(planilha.iat[6, coluna])
        if nivel in ("Ensino fundamental", "Ensino médio"):
            modalidade = MODALIDADES_DA_FONTE[subcategoria]
        elif nivel == "Mestrado e doutorado":
            modalidade = nivel_original
        else:
            modalidade = "Geral"
        colunas.append((coluna, nivel, modalidade))
    return colunas


def extrair_aba(planilha, ano):
    colunas = colunas_dos_indicadores(planilha, ano)
    registros = []
    for indice, linha in enumerate(planilha.itertuples(index=False, name=None)):
        if indice < 8:
            continue
        rotulo = texto(linha[0])
        if rotulo in ("Rio de Janeiro", "Rio de Janeiro (1)"):
            escopo, codigo, territorio = "municipio", "", "Rio de Janeiro"
        else:
            regiao = PADRAO_RA.fullmatch(rotulo)
            if regiao is None:
                continue
            codigo, nome = regiao.groups()
            escopo = "regiao"
            territorio = NOMES_REGIONAIS.get(nome, nome)

        for coluna, nivel, modalidade in colunas:
            estimativa, status = interpretar_valor(linha[coluna], ano)
            registros.append({
                "ano": ano,
                "escopo": escopo,
                "ra_codigo": codigo,
                "territorio": territorio,
                "nivel_ensino": nivel,
                "modalidade": modalidade,
                "estudantes_estimados": estimativa,
                "status_origem": status,
                "linha_origem": indice + 1,
                "coluna_origem": colname(coluna),
            })
    return pd.DataFrame.from_records(registros)


def carregar_tabela(caminho=ARQUIVO_BRUTO):
    """Lê as duas abas originais e valida a chave de cada estimativa."""
    abas = pd.read_excel(
        caminho, sheet_name=[str(ano) for ano in ANOS],
        engine="xlrd", header=None, keep_default_na=False,
    )
    dados = pd.concat(
        [extrair_aba(abas[str(ano)], ano) for ano in ANOS],
        ignore_index=True,
    )
    chave = ["ano", "escopo", "ra_codigo", "nivel_ensino", "modalidade"]
    totais_municipais = dados.loc[
        (dados["escopo"] == "municipio") & (dados["nivel_ensino"] == "Total")
    ]
    if dados.duplicated(chave).any() or tuple(totais_municipais["ano"]) != ANOS:
        raise ValueError("Chave duplicada ou total municipal ausente na fonte.")
    return dados


def salvar_tabela(dados, destino=ARQUIVO_TRATADO):
    """Grava o CSV com gzip determinístico e troca o arquivo ao final."""
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=destino.parent, delete=False) as temporario:
        pendente = Path(temporario.name)
        try:
            dados.to_csv(
                temporario, index=False, encoding="utf-8", lineterminator="\n",
                compression={"method": "gzip", "mtime": 0, "filename": ""},
            )
        except BaseException:
            temporario.close()
            pendente.unlink(missing_ok=True)
            raise
    try:
        pendente.replace(destino)
    finally:
        pendente.unlink(missing_ok=True)
    return destino


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, default=ARQUIVO_BRUTO)
    parser.add_argument("--saida", type=Path, default=ARQUIVO_TRATADO)
    args = parser.parse_args()
    dados = carregar_tabela(args.entrada)
    caminho = salvar_tabela(dados, args.saida)
    print(f"{len(dados)} registros gravados em {caminho}")


if __name__ == "__main__":
    main()
