(() => {
    "use strict";

    const avisoArtigo = document.getElementById("vice-city-artigo");
    const script = document.currentScript;
    const painelNotebook = script?.closest("[data-vice-notebook]")
        ?? script?.parentElement?.querySelector("[data-vice-notebook]")
        ?? document.querySelector("[data-vice-notebook]");
    const aviso = avisoArtigo ?? painelNotebook?.querySelector(".vice-city-aviso");
    if (!aviso) return;

    const raiz = painelNotebook?.closest(".jp-Notebook, #notebook-container") ?? document.documentElement;
    const modo = avisoArtigo ? "artigo" : "notebook";
    const chave = Symbol.for("lp6.vice-city");
    raiz[chave]?.abort();
    const controle = new AbortController();
    raiz[chave] = controle;

    const eventos = { capture: true, signal: controle.signal };
    const codigo = "iddqd";
    const autor = [...raiz.querySelectorAll("strong")].find(
        (elemento) => elemento.textContent.trim() === "Guilherme Familiar do Amaral"
    );
    const editavel = "input, textarea, select, [contenteditable]:not([contenteditable=false]), .cm-editor, .monaco-editor";
    let progresso = 0;
    let toques = 0;
    let ultimoToque = 0;

    function limparSequencia() {
        progresso = 0;
        toques = 0;
        ultimoToque = 0;
    }

    function atualizarAviso() {
        const ativo = raiz.dataset.viceCity === modo;
        aviso.hidden = !ativo;
        aviso.textContent = ativo ? "VICE CITY · 5 toques no nome ou Shift + IDDQD para voltar" : "";
    }

    function alternarTema() {
        if (raiz.dataset.viceCity !== modo) {
            raiz.dataset.viceCity = modo;
        } else {
            delete raiz.dataset.viceCity;
        }
        atualizarAviso();
    }

    atualizarAviso();

    if (autor) {
        autor.style.touchAction = "manipulation";
        autor.style.userSelect = "none";
        autor.style.webkitUserSelect = "none";
        autor.addEventListener("click", (evento) => {
            toques = evento.timeStamp - ultimoToque <= 650 ? toques + 1 : 1;
            ultimoToque = evento.timeStamp;
            if (toques === 5) {
                limparSequencia();
                alternarTema();
            }
        }, eventos);
    }

    raiz.addEventListener("keydown", (evento) => {
        if (!aviso.isConnected) {
            controle.abort();
            return;
        }
        if (evento.key === "Shift" || evento.repeat) return;
        if (!evento.shiftKey || evento.ctrlKey || evento.altKey || evento.metaKey ||
            evento.isComposing || evento.composedPath().some((alvo) => alvo.matches?.(editavel))) {
            limparSequencia();
            return;
        }

        const letra = evento.key.toLowerCase();
        if (letra === codigo[progresso]) {
            progresso += 1;
        } else {
            progresso = letra === codigo[0] ? 1 : 0;
        }
        if (progresso === codigo.length) {
            evento.preventDefault();
            limparSequencia();
            alternarTema();
        }
    }, eventos);

    raiz.addEventListener("focusout", limparSequencia, eventos);
    window.addEventListener("blur", limparSequencia, eventos);
})();
