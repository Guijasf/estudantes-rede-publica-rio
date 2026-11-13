"use strict";

const pagina = window.location;
const sufixoGitHub = ".github.io";
if (pagina.hostname.endsWith(sufixoGitHub)) {
    const conta = pagina.hostname.slice(0, -sufixoGitHub.length);
    const primeiroSegmento = pagina.pathname.split("/").filter(Boolean)[0];
    const nome = primeiroSegmento && primeiroSegmento !== "index.html"
        ? primeiroSegmento
        : pagina.hostname;
    const repositorio = `https://github.com/${conta}/${nome}`;
    const atalho = document.querySelector("#repositorio");
    atalho.href = repositorio;
    atalho.textContent = "Repositório no GitHub";
    document.querySelector("#clone").textContent = `git clone ${repositorio}.git estudantes-rede-publica-rio`;
}

const indicador = document.querySelector("#indicador");
const ordem = document.querySelector("#ordem");
const corpo = document.querySelector("#regioes-dados");
const resumo = document.querySelector("#regioes-resumo");
const inteiro = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
const diferenca = new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 0,
    signDisplay: "exceptZero"
});
const percentual = new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    signDisplay: "exceptZero"
});

function mostrarRegioes() {
    const linhas = [...DADOS_REGIONAIS[indicador.value]];
    const campo = ordem.value === "percentual" ? "variacao_pct" : "diferenca";
    const direcao = ordem.value === "quedas" ? 1 : -1;
    linhas.sort((a, b) => direcao * (a[campo] - b[campo]));
    const elementos = linhas.map((registro) => {
        const linha = document.createElement("tr");
        const celulas = [
            `${registro.ra_codigo} · ${registro.territorio}`,
            inteiro.format(registro["2000"]),
            inteiro.format(registro["2010"]),
            diferenca.format(registro.diferenca),
            `${percentual.format(registro.variacao_pct)}%`
        ];
        celulas.forEach((valor, indice) => {
            const celula = document.createElement(indice === 0 ? "th" : "td");
            if (indice === 0) celula.scope = "row";
            celula.textContent = valor;
            linha.append(celula);
        });
        return linha;
    });
    corpo.replaceChildren(...elementos);
    resumo.textContent = `${linhas.length} regiões · ${indicador.selectedOptions[0].textContent}`;
}

indicador.addEventListener("change", mostrarRegioes);
ordem.addEventListener("change", mostrarRegioes);
mostrarRegioes();
