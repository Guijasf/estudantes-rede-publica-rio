# Dicionário de dados da Tabela 892

A Tabela 892 contém estimativas do número de estudantes da rede pública por nível e modalidade de ensino no município do Rio de Janeiro e em suas Regiões Administrativas. A Prefeitura da Cidade do Rio de Janeiro publica o arquivo no Data.Rio. As duas abas citam as amostras dos Censos Demográficos do IBGE e a aba de 2000 menciona o Banco Multidimensional de Estatísticas. [Ficha e licença no Data.Rio](https://www.data.rio/documents/6b99c568d38646bb97dcf2751c501e7f/about)

## Arquivos e granularidade

| Arquivo | Formato | Conteúdo |
| --- | --- | --- |
| `raw/tabela_892.xls` | Excel 97–2003 | Original baixado do Data.Rio, com abas `2000` e `2010`. |
| `processed/estudantes.csv.gz` | CSV UTF-8 comprimido com gzip | Uma linha por célula de estimativa do original, identificada por ano, escopo, código da RA, nível e modalidade. |

A planilha original tem SHA-256 `df4717c72e03073f4ce63ef5d4b7925c631aeb73451d2e5195b26e5f9e063046`. O [download oficial](https://www.arcgis.com/sharing/rest/content/items/6b99c568d38646bb97dcf2751c501e7f/data) é público.

## Variáveis

| Coluna | Tipo e formato | Significado |
| --- | --- | --- |
| `ano` | Inteiro de quatro dígitos | Ano do Censo e nome da aba de origem, 2000 ou 2010. |
| `escopo` | Texto enumerado | `municipio` para o agregado oficial da cidade ou `regiao` para uma RA. |
| `ra_codigo` | Texto, algarismos romanos | Código da RA na planilha. Campo vazio nas linhas municipais. |
| `territorio` | Texto UTF-8 | Nome da RA ou Rio de Janeiro. Espaços foram normalizados e as grafias Ilha do Governador e Santa Teresa foram corrigidas. |
| `nivel_ensino` | Texto UTF-8 | Nível padronizado para comparação. `Total` identifica o total publicado para o território e o ano. |
| `modalidade` | Texto UTF-8 | Detalhe de ensino regular, supletivo ou pós-graduação. `Geral` indica nível sem detalhamento adicional na aba. `Total publicado` identifica o agregado da fonte. |
| `estudantes_estimados` | Número decimal, ponto como separador decimal | Estimativa do número de estudantes. A precisão da fonte é preservada no CSV. A célula fica vazia quando a estimativa está indisponível. |
| `status_origem` | Texto enumerado | `informado` indica valor numérico. `indisponivel` identifica `...` em 2000. `zero_explicito` identifica `-` em 2010, zero segundo a nota da aba. |
| `linha_origem` | Inteiro positivo | Número da linha na aba Excel, contado a partir de 1. |
| `coluna_origem` | Texto de uma letra | Letra da coluna Excel da estimativa. |

## Regras de comparação

| Indicador | 2000 | 2010 |
| --- | --- | --- |
| Fundamental e médio | Regular seriado, regular não seriado e supletivo | Regular e supletivo |
| Mestrado e doutorado | Categoria combinada | Soma das duas categorias |
| Pré-vestibular | Categoria própria | Sem coluna correspondente |
| Especialização | Sem coluna correspondente | Categoria própria |

As comparações por nível somam as modalidades do mesmo nível e mantêm a estimativa ausente quando alguma parcela está indisponível. As categorias sem correspondente ficam disponíveis no CSV para consulta. A análise usa o total publicado para cada território. Em 2000, a soma dos totais regionais fica 196 abaixo do total municipal publicado. A fonte registra possíveis diferenças entre parcelas e totais por se tratar de dados da amostra.

As abas têm 32 e 33 RAs. Vigário Geral (XXXI) tem linha própria em 2010. Uma tabela municipal com a população do Censo 2000 apresenta os bairros de Vigário Geral dentro de Penha (XI). O Plano Diretor de 2011 registra as duas RAs separadamente. A análise principal usa 31 RAs com observações nos dois anos e retira Penha e Vigário Geral do ranking individual. Como análise complementar, compara Penha de 2000 à soma de Penha e Vigário Geral de 2010, sob a hipótese de cobertura equivalente. [Tabela municipal com o recorte de 2000](https://www.rio.rj.gov.br/dlstatic/10112/413631/DLFE-220680.pdf/1.0) · [Plano Diretor de 2011](https://www.rio.rj.gov.br/dlstatic/10112/3678296/4353007/PlanoDiretorLC111_2011)

A diferença em estudantes estimados é o valor de 2010 menos o de 2000. A variação percentual divide essa diferença pelo valor de 2000 e multiplica por 100, quando o denominador é positivo.

## Atribuição

Prefeitura da Cidade do Rio de Janeiro, Data.Rio, Tabela 892. Fonte estatística IBGE, Censos Demográficos 2000 e 2010, amostras. Dados publicados sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). A versão processada é uma transformação para formato longo, com padronização de nomes, níveis e marcadores de ausência ou zero.
