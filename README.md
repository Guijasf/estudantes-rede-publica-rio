# Estudantes da rede pública do Rio de Janeiro em 2000 e 2010

![Python 3.12](https://img.shields.io/badge/Python-3.12-306998)
![Código MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-17665d)
![Dados CC BY 4.0](https://img.shields.io/badge/dados-CC%20BY%204.0-17665d)

- **Autor** Guilherme Familiar do Amaral
- **Orientador** Alexandre Neves Louzada
- **Instituição** Centro Universitário La Salle do Rio de Janeiro (Unilasalle-RJ)
- **Curso** Bacharelado em Sistemas de Informação
- **Disciplina** Linguagem de Programação · 6º período · 2026.2

Este trabalho analisa o número estimado de estudantes da rede pública no município do Rio de Janeiro nos Censos de 2000 e 2010. O total municipal cresceu **12,5%**. Entre os níveis comparáveis, o ensino médio teve o maior ganho absoluto, de cerca de **72,6 mil** estudantes. O número estimado de estudantes em creches passou de **21.799** para **47.706**. A análise regional compara 31 RAs individualmente e examina Penha e Vigário Geral em uma comparação territorial complementar.

**Palavras-chave** educação pública, Censo Demográfico, regiões administrativas, creche, Rio de Janeiro.

[Fonte original no Data.Rio](https://www.data.rio/documents/6b99c568d38646bb97dcf2751c501e7f/about) · [Notebook](notebooks/analise_exploratoria.ipynb) · [Artigo em HTML](docs/index.html) · [Dicionário de dados](data/data_dictionary.md)

## Estrutura do projeto final

| Caminho | Conteúdo |
| --- | --- |
| `data/raw/tabela_892.xls` | Planilha original com as abas dos dois censos. |
| `data/processed/estudantes.csv.gz` | Estimativas tratadas em CSV comprimido. |
| `data/data_dictionary.md` | Significado dos campos, origem e regras de tratamento. |
| `src/etl.py` | Leitura, limpeza, validação e exportação dos dados. |
| `src/analise.py` | Cálculo dos indicadores e geração das visualizações. |
| `notebooks/analise_exploratoria.ipynb` | Análise das três perguntas com as saídas executadas. |
| `docs/index.html` e `docs/assets/` | Artigo acadêmico e seus gráficos e recursos. |

## Perguntas de pesquisa

1. Como o número estimado de estudantes da rede pública mudou no município entre 2000 e 2010, por nível de ensino comparável?
2. Quais Regiões Administrativas tiveram os maiores aumentos e quedas no total de estudantes entre os dois censos?
3. Em quais Regiões Administrativas se concentrou o crescimento do número estimado de estudantes em creches públicas?

## Reprodução

Use o Python 3.12 e abra um terminal na pasta que contém o `README.md`. A planilha original acompanha o projeto. As versões das bibliotecas de análise, do kernel do notebook e de suas dependências estão fixadas em `requirements.txt`.

No Windows, execute no PowerShell.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.analise
```

No macOS ou Linux, execute os comandos abaixo.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.analise
```

O comando `python -m src.analise` reconstrói `data/processed/estudantes.csv.gz`, as três figuras e os dados da tabela interativa em `docs/assets/`. Para executar somente a transformação dos dados, use `python -m src.etl` no ambiente virtual.

No VS Code, com as extensões Python e Jupyter, abra `notebooks/analise_exploratoria.ipynb`. Em **Selecionar Kernel**, escolha o ambiente `.venv` criado acima e clique em **Executar Tudo**.

## Artigo e publicação

O artigo fica em `docs/index.html` e pode ser aberto diretamente no navegador. A tabela regional permite escolher o indicador e a ordenação.

Envie o conteúdo desta pasta para a raiz de um repositório público no GitHub. Depois do primeiro push, acesse **Settings → Pages**, selecione **Deploy from a branch**, escolha `main` e `/docs` e clique em **Save**. A URL do artigo aparece nessa tela após a publicação. [Documentação do GitHub Pages](https://docs.github.com/pt/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Dados e licença

A Tabela 892 foi publicada pela Prefeitura da Cidade do Rio de Janeiro no Data.Rio, com base nas amostras dos Censos Demográficos 2000 e 2010 do IBGE. A publicação original indica licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). As transformações e a atribuição estão registradas no [dicionário](data/data_dictionary.md). A [licença MIT](LICENSE) se aplica ao código do projeto.
