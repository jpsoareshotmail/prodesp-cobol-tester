# Email de Solicitacao - Prodesp

---

**Para:** Equipe Tecnica Prodesp
**CC:** Gestao do Projeto BRQ
**Assunto:** Solicitacao de artefatos para validacao dos programas COBOL convertidos

---

Prezados,

Analisamos a amostragem entregue (pasta "Amostragem POC - Fontes Convertidos",
subpastas Convertidos e Originais). Abaixo o resultado da conferencia e os
artefatos ainda necessarios para concluir a compilacao e a validacao dos
programas COBOL convertidos.

---

## 1. Conferencia dos copybooks entregues

A pasta Convertidos contem 56 arquivos. Analisando o conteudo de cada arquivo
(nao apenas o nome): **42 sao programas e 14 sao copybooks**, todos de tela/mapa
(layout de telas: placa, chassi, autenticacoes, mensagens).

**Copybooks de tela na pasta (14):**
AUML01, CAPA01, CCCC99, COFI02, COFI04, COFI11, EMIS98, EMIS99, EMPA01,
GERA01, MENS01, MENS03, RENA01, RENA04.

Destes, 13 sao efetivamente usados pelos programas via COPY.

**Observacao (divergencia de nome):** o arquivo AUML01 esta na pasta, porem
nenhum programa faz `COPY AUML01`. Os programas referenciam `AUMI01` (com "I"),
que nao consta na entrega. Favor confirmar se AUML01 e AUMI01 sao o mesmo
copybook (erro de digitacao) ou copybooks distintos.

---

## 2. Copybooks de dados/banco FALTANTES (217)

O que ainda impede a compilacao sao os **copybooks de dados/banco** - definicao
das estruturas das tabelas DB2/DMS e rotinas de acesso a dados. **Nenhum deles
veio na amostragem.** Sao referenciados via instrucao COPY dentro dos proprios
programas (ex.: o programa OGAA640D possui 144 instrucoes COPY).

**Total referenciado nos fontes:** 230 copybooks distintos
**Recebidos (presentes na pasta e usados):** 13
**FALTANTES:** 217

**Familias faltantes:**

| Familia | Qtd | Descricao |
|---------|-----|-----------|
| WSGL / PDGL / WSGLDB / PDGLDB | 4 | Variaveis globais - usados por TODOS os 42 programas |
| WSD01xxx / PDD01xxx (e 06/07/12/14/21) | 162 | Definicao e acesso as tabelas DB2 |
| WSBLQ / PDBLQ | 16 | Bloqueios (inclui WSBLQ026 - dataset RENAJUDDS) |
| WSFUR / PDFUR | 6 | Registros de furto |
| WSTAB / PDTAB | 8 | Tabelas auxiliares |
| WSADM / PDADM | 2 | Administracao |
| WSALG | 1 | Algoritmo |
| COMS / COMSIN / COMSOUT / CONT* | 6 | Runtime online |
| SEECDT00 / SEECDTPD | 2 | Biblioteca DMS |
| CODIGOS, COFI01/03/10, EMIS02/03, EMPA03, EMPB01, AUMI01, SPLC01 | 10 | Diversos |

**Exemplo de referencia (esclarecimento sobre WSBLQ026):**
o copybook WSBLQ026 e chamado via `COPY WSBLQ026.` na linha 92 dos programas
FGAT006D e FGAT030D (dataset RENAJUDDS). Nao consta na entrega.

A lista completa dos 217 faltantes, com o(s) fonte(s) que referenciam cada um,
segue no anexo **COPYBOOKS_FALTANTES.md / COPYBOOKS_FALTANTES.csv**.

**Formato de entrega desejado:** arquivos texto (.cpy), extraidos da biblioteca
de COPY do ambiente Unisys/Micro Focus.

---

## 3. DDL das tabelas (formato DB2)

Precisamos da estrutura das tabelas para criar o banco de testes DB2. Se a DDL
em formato DB2 ja existir (gerada no processo de conversao), enviar diretamente.
Caso contrario, a definicao das tabelas do DMS atual serve para convertermos.

**Tabelas identificadas nos programas (34):**

ALERTADS, AUTENTICACAODS, AVARIADOSDS, BLINDADOSDS, BLOQUEIODS, CAMBIODS,
CNPJOFICIALDS, CODSEGCRLVDS, CODSEGCRVDS, COMVENDS, CSVCERTDS, DESBLOQUEIODS,
DESPACHANTEDS, DETTABDS, ECRVAUTENTICADS, ESCPLACDS, ESPELHODS, ESTAMPAGEMDS,
GEVERDS, GEVEXCLUIDODS, GEVMODIFDS, GRAVAMESDS, INSPECAODS, LACRACAODS,
MODIFICADODS, NOVAPLACDS, OBSERVCRLVDS, PRODPLCDS, PRODPLIDS, QUEIXADS,
RECUPERADODS, RENAVEDS, TABMUNBRDS, TAXADS, TAXASDS, USUARIODS, VALIDACAODS,
VISTORIADS

**Formato de entrega:** scripts CREATE TABLE ou documento com nome das colunas,
tipos e tamanhos de cada tabela.

---

## 4. Amostra de dados de teste

Registros de exemplo (5 a 10 por tabela) para alimentar o banco de testes e
validar as consultas dos programas.

**Formato de entrega:** INSERT scripts, CSV, ou export do banco atual (dados
anonimizados se necessario).

---

## 5. Confirmacao de versao dos fontes

Os fontes convertidos que recebemos sao versao 4.1 (setembro/2024). Os fontes
originais sao versao 6.1 (maio/2026) e possuem patches de faixas de placa
adicionados em 2025/2026 (UDA-UGV, UOG-USB, TIO-TMJ).

**Pergunta:** Os fontes convertidos devem receber esses patches antes da
migracao para z/OS, ou serao aplicados apos a migracao?

---

## Resumo do impacto

- Item **1** ja atendido (copybooks de tela OK; confirmar apenas AUML01/AUMI01).
- Item **2** (217 copybooks de dados) e o principal bloqueio: sem eles, os 16
  programas restantes nao compilam e os demais nao tem os campos completos.
- Itens **3 e 4** (DDL + massa) sao necessarios para validar comportamento
  (execucao das queries), nao apenas a compilacao.
- Item **5** define o escopo correto da versao a migrar.

Fico a disposicao para esclarecer qualquer ponto.

Atenciosamente,
Jenner Soares
Equipe BRQ
