# Checklist PRISMA 2020

Verificação dos 27 itens do checklist PRISMA 2020 contra o manuscrito atual.

Referência: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement.
BMJ. 2021;372:n71.

Status: `[x]` completo | `[~]` parcial | `[ ]` ausente

Caminhos relativos a `revisao-sistematica/`. Linhas referem-se ao estado do
manuscrito em 2026-04-06.

## Título e Resumo

| #  | Item                                            | Status | Localização                                  |
|----|-------------------------------------------------|--------|----------------------------------------------|
| 1  | Identificar como revisão sistemática            | [x]    | `manuscrito/main.tex:164-165` (título contém "Revisão Sistemática da Literatura") |
| 2  | Resumo estruturado (PRISMA 2020 Abstract)       | [x]    | `manuscrito/main.tex:178-216` (Contexto, Objetivo, Método, Resultados, Conclusão) |

## Introdução

| #  | Item                                            | Status | Localização                                  |
|----|-------------------------------------------------|--------|----------------------------------------------|
| 3  | Justificativa (rationale)                       | [x]    | `manuscrito/secoes/introducao.tex:7-58`; posicionamento contra trabalhos anteriores em `manuscrito/secoes/trabalhos-relacionados.tex:1-132` |
| 4  | Objetivos (questão principal + QS1-QS5)         | [x]    | `manuscrito/secoes/introducao.tex:60-107` |

## Métodos

| #   | Item                                           | Status | Localização                                  |
|-----|------------------------------------------------|--------|----------------------------------------------|
| 5   | Critérios de elegibilidade                     | [x]    | `manuscrito/secoes/metodo.tex:23-75` (PICo + Tabela CI/CE) |
| 6   | Fontes de informação                           | [x]    | `manuscrito/secoes/metodo.tex:77-97` (Scopus, arXiv, Semantic Scholar, datas) |
| 7   | Estratégia de busca completa                   | [x]    | `manuscrito/secoes/metodo.tex:99-128` (string Scopus em footnote, restante em material suplementar) |
| 8   | Processo de seleção                            | [x]    | `manuscrito/secoes/metodo.tex:158-173` |
| 9   | Processo de coleta de dados                    | [x]    | `manuscrito/secoes/metodo.tex:175-192` |
| 10  | Itens de dados                                 | [x]    | `manuscrito/secoes/metodo.tex:175-192` (37 campos, 7 categorias); detalhamento em `extracao/formulario-extracao.md` |
| 11  | Avaliação de risco de viés / qualidade         | [x]    | `manuscrito/secoes/metodo.tex:194-212` (checklist Q1-Q6 adaptado de Kitchenham) |
| 12  | Medidas de efeito                              | [x]    | `manuscrito/secoes/metodo.tex:220-223` — declaraç��o explícita: síntese narrativa, medidas restritas a Pass@1 e delta-pp |
| 13a | Síntese — elegibilidade para cada síntese      | [x]    | `manuscrito/secoes/metodo.tex:214-220` (organização por QS1-QS5) |
| 13b | Síntese — preparação dos dados                 | [x]    | `manuscrito/secoes/metodo.tex:182-192` (vocabulário controlado, NR/NA, validação enum) |
| 13c | Síntese — tabulação/visualização               | [x]    | `manuscrito/secoes/metodo.tex:214-220`; tabelas e figuras descritas em `manuscrito/secoes/resultados.tex` |
| 13d | Síntese — métodos de síntese                   | [x]    | `manuscrito/secoes/metodo.tex:214-220` (síntese narrativa temática; meta-análise descartada com justificativa) |
| 13e | Exploração de heterogeneidade                  | [x]    | `manuscrito/secoes/metodo.tex:217-220`; resultados em `manuscrito/secoes/resultados.tex:230-236` (heterogeneidade de modelo, subset, parâmetros) |
| 13f | Análises de sensibilidade                      | [x]    | `manuscrito/secoes/metodo.tex:222-227` (S1 venues revisados, S2 exclusão de baixa qualidade) |
| 14  | Avaliação de viés de reporte                   | [x]    | `manuscrito/secoes/metodo.tex:229-232` (não aplicável a síntese narrativa; predomínio de preprints reconhecido) |
| 15  | Avaliação de certeza                           | [x]    | `manuscrito/secoes/metodo.tex:233-237` (alta/moderada/baixa por achado) |

## Resultados

| #   | Item                                           | Status | Localização                                  |
|-----|------------------------------------------------|--------|----------------------------------------------|
| 16a | Seleção de estudos (fluxo PRISMA + razões)     | [x]    | `manuscrito/secoes/resultados.tex:4-23` + diagrama PRISMA via `analise/diagrama-fluxo-prisma.tex` |
| 16b | Lista de excluídos no texto completo + razões  | [x]    | `manuscrito/secoes/resultados.tex:16-22` — totais por critério + referência ao pacote de replicação (DOI) com lista detalhada |
| 17  | Características dos estudos incluídos          | [x]    | `manuscrito/secoes/resultados.tex:25-93` (`tab:caracteristicas`) |
| 18  | Risco de viés / qualidade dos estudos          | [x]    | `manuscrito/secoes/resultados.tex:95-104` (distribuição de scores Q1-Q6) |
| 19  | Resultados dos estudos individuais             | [x]    | `manuscrito/secoes/resultados.tex:250-278` (`tab:desempenho` com base/mem/ganho por estudo) |
| 20a | Síntese — características + risco              | [x]    | `manuscrito/secoes/resultados.tex:106-186` (QS1) e `:188-236` (QS2) com cross-ref para tabelas de características e qualidade |
| 20b | Síntese — resultados de cada síntese           | [x]    | `manuscrito/secoes/resultados.tex:106-476` (QS1-QS5 com tabelas e figuras) |
| 20c | Síntese — heterogeneidade                      | [x]    | `manuscrito/secoes/resultados.tex:230-236, 280-294, 458-470` (rendimentos decrescentes, consistência cross-LLM, complexidade-vs-ganho) |
| 20d | Síntese — sensibilidade                        | [x]    | `manuscrito/secoes/resultados.tex:478-491` (S1 e S2) |
| 21  | Viés de reporte por síntese                    | [x]    | `manuscrito/secoes/resultados.tex:563-572` — parágrafo dedicado: preprint dominance (82%) como risco para QS4/QS2, S1 não inverteu achados, risco contido para alta certeza, não descartável para moderada/baixa |
| 22  | Certeza da evidência por achado                | [x]    | `manuscrito/secoes/resultados.tex:493-542` (`tab:certeza`, 19 achados) |

## Discussão

| #   | Item                                           | Status | Localização                                  |
|-----|------------------------------------------------|--------|----------------------------------------------|
| 23a | Interpretação geral no contexto da evidência   | [x]    | `manuscrito/secoes/discussao.tex:7-57` (Principais achados) e posicionamento em `manuscrito/secoes/trabalhos-relacionados.tex:60-132` |
| 23b | Limitações da evidência incluída               | [x]    | `manuscrito/secoes/discussao.tex:153-163, 179-184` (preprints 82%, heterogeneidade SWE-bench Verified) |
| 23c | Limitações dos processos da revisão            | [x]    | `manuscrito/secoes/discussao.tex:165-208` (triagem por um pesquisador, duas bases, extração single-rater) |
| 23d | Implicações para prática, política, pesquisa   | [x]    | `manuscrito/secoes/discussao.tex:59-148` (implicações pesquisa + prática) e `:210-242` (direções futuras) |

## Outras Informações

| #   | Item                                           | Status | Localização                                  |
|-----|------------------------------------------------|--------|----------------------------------------------|
| 24a | Registro                                       | [x]    | `manuscrito/main.tex:231-236` (não registrado em PROSPERO; justificativa explícita) |
| 24b | Disponibilidade do protocolo                   | [x]    | `manuscrito/main.tex:231-236` — protocolo no pacote de replicação (DOI: 10.5281/zenodo.19463131) |
| 24c | Emendas ao protocolo                           | [x]    | `manuscrito/secoes/metodo.tex:19-21` ("Seis emendas foram registradas durante a execução"); detalhe em `protocolo/emendas.md` |
| 25  | Apoio / financiamento                          | [x]    | `manuscrito/main.tex:238-240` |
| 26  | Conflitos de interesse                         | [x]    | `manuscrito/main.tex:242-243` |
| 27  | Disponibilidade de dados, código e materiais   | [x]    | `manuscrito/main.tex:245-250` — DOI: 10.5281/zenodo.19463131 + mirror GitHub público |

## Resumo

**Totais:**

- Completos `[x]`: **27**
- Parciais `[~]`: **0**
- Ausentes `[ ]`: **0**

Total geral: 27/27 completos.

**Itens a corrigir antes da submissão:**

1. **Item 12 (medidas de efeito)** — adicionar declaração explícita em
   `manuscrito/secoes/metodo.tex:214-220` informando que, por se tratar de
   síntese narrativa, as medidas reportadas restringem-se a Pass@1 e Δpp
   absoluto sem effect size formal.
2. **Item 16b (lista de excluídos no texto completo)** — referenciar
   `triagem/triagem-texto-completo.tsv` como material suplementar em
   `manuscrito/secoes/resultados.tex` (subseção de seleção) ou incluir
   apêndice com os 23 estudos excluídos e suas razões. Hoje apenas o total
   por critério é reportado.
3. **Item 21 (viés de reporte por síntese)** — adicionar nota por QS em
   `manuscrito/secoes/resultados.tex` indicando que o predomínio de
   preprints (82%) é potencial fonte de viés de reporte para QS3 e QS4
   (custos), conectando explicitamente ao impacto observado em S1.
4. **Item 24b (protocolo)** — substituir "disponível sob solicitação" em
   `manuscrito/main.tex:234-236` por link público estável (repositório
   versionado, OSF, Zenodo) para `protocolo/protocolo-v1.md`.
5. **Item 27 (dados/código/materiais)** — substituir "mediante solicitação
   razoável" em `manuscrito/main.tex:245-250` por DOI/URL público para os
   artefatos versionados (`busca/`, `triagem/`, `extracao/`, `analise/`)
   após publicação do pacote de replicação no Zenodo.

Nenhum item está completamente ausente. As cinco lacunas são todas de
"reforço de transparência" e podem ser endereçadas por edições pontuais
em `manuscrito/main.tex` e `manuscrito/secoes/{metodo,resultados}.tex`,
sem necessidade de nova análise ou re-extração de dados.
