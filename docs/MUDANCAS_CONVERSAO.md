# Mudancas da Conversao: Original (Unisys/Micro Focus) → Convertido (GnuCOBOL)

## Resumo

Os fontes convertidos NAO foram alterados. Todas as adaptacoes foram feitas no
**ambiente de compilacao** (copybooks, stubs, pre-processador).

---

## 1. Mudancas no Fonte Convertido (feitas pelo processo de conversao original)

Estas mudancas ja vieram no arquivo convertido (pasta `fontes_convertidos/Convertidos/`):

| # | Mudanca | Exemplo Original | Exemplo Convertido |
|---|---------|-----------------|-------------------|
| 1 | Remocao de numeros de linha (col 1-6) | `001000 IDENTIFICATION...` | `       IDENTIFICATION...` |
| 2 | Remocao de diretivas $$SET | `$$SET SHARING=SHAREDBYALL` | `*$$SET SHARING=SHAREDBYALL  *GOT*` |
| 3 | PROGRAM-ID descomentado e renomeado | `*PROGRAM-ID. PC-GAA-L004.` | `PROGRAM-ID. FGAA004.` |
| 4 | NOT IS → IS NOT (padrao ANSI) | `LC-MILHAR NOT IS NUMERIC` | `LC-MILHAR IS NOT NUMERIC  *GOT*` |
| 5 | Adicionado COPY WSGL (Working-Storage Global) | (nao existia) | `COPY WSGL.` |
| 6 | Adicionado COPY PDGL (Procedure Div Global) | (nao existia) | `COPY PDGL.` |
| 7 | Adicionado COPY WSGLDB (para programas com DB) | (nao existia) | `COPY WSGLDB.` |
| 8 | Adicionado COPY PDGLDB (para programas com DB) | (nao existia) | `COPY PDGLDB.` |
| 9 | OBJECT-COMPUTER comentado | `OBJECT-COMPUTER. A15.` | `* OBJECT-COMPUTER. A15.  *GOT*` |
| 10 | Marcador *GOT* em linhas alteradas | (nao existia) | `*GOT*` na coluna 73+ |

---

## 2. Ambiente de Compilacao Criado (NAO altera os fontes)

Para compilar os fontes convertidos sem modifica-los, criamos:

### 2.1 Copybooks Globais (cobol_build/copy/)

| Copybook | Funcao | Conteudo |
|----------|--------|----------|
| WSGL.cpy | Variaveis globais Working-Storage | WS-RETURN-CODE, WS-ERROR-FLAG, C-MAPA, MYSELF/TASKVALUE |
| WSGLDB.cpy | Variaveis globais de banco | SQLCODE, DATABASE-OPEN-MODE, DMSTATUS-S, ROUTINE-REF |
| PDGL.cpy | Paragrafo global de saida | 9999-GLOBAL-EXIT / EXIT PROGRAM |
| PDGLDB.cpy | 300+ paragrafos de runtime DB/DMS | xxxDS-CR, -ST, -DL, -LOCK, -RECR, -STBG, -STEN, -DB2DMS |
| CODIGOS.cpy | Tabela de codigos de retorno | C-RETORNO, C-MENSAGEM, C-PROGRAMA |
| WSGL-DATASETS.cpy | 2071 campos de 65 datasets | Definicoes de record areas (ALE-*, QXA-*, GER-*, etc.) |

### 2.2 Copybooks de Tabelas (224 stubs)

Cada `WSDxxxxx.cpy` e `PDDxxxxx.cpy` contem stubs minimos para que o compilador
nao rejeite os `COPY` statements. Os campos reais estao no WSGL-DATASETS.cpy.

### 2.3 Copybooks de Fontes Faltantes (fontes_faltanters/)

Copiados e adaptados para formato fixo:
- SEECDT00.cpy — Smart Change date fields (Y2K)
- SEECDTPD.cpy — Procedure division do SEEC
- LIB_GRAVAMES.cpy, LIB_RENAVAM.cpy — Bibliotecas de negocio

---

## 3. Pre-processador SQL (app/sql_preprocessor.py)

O pre-processador gera um arquivo temporario (_processed) para compilacao.
O fonte original permanece intacto no disco.

### Acoes do pre-processador:

| # | Acao | Motivo |
|---|------|--------|
| 1 | Comenta blocos EXEC SQL ... END-EXEC | GnuCOBOL nao tem pre-compilador DB2 nativo |
| 2 | Comenta blocos EXEC CICS ... END-EXEC | GnuCOBOL nao tem runtime CICS |
| 3 | Adiciona CONTINUE apos bloco comentado | Manter fluxo de controle |
| 4 | Preserva ponto final (.) quando original tinha | Fechar IF/ELSE abertos |
| 5 | Comenta PERFORM DATABASE-OPEN/CLOSE/TERMINATE | Chamadas de runtime DMS |
| 6 | Comenta CALL SYSTEM DMTERMINATE | Chamada de shutdown DMS |
| 7 | Comenta PERFORM xxx-STEN (statements) | Operacoes de cursor DMS |
| 8 | Comenta PERFORM com qualificador :TRUE | Sintaxe Micro Focus de secao |
| 9 | Preserva nomes de paragrafos antes de EXEC SQL | Manter estrutura procedural |

---

## 4. Auto-fix Iterativo (fix_all_errors.py)

Quando a compilacao falha com "is not defined", o sistema:
1. Extrai nomes de variaveis/paragrafos nao definidos
2. Adiciona declaracoes (01 VARNAME PIC X(050)) no Working-Storage
3. Adiciona paragrafos (PARANAME. CONTINUE.) antes do COPY PDGL
4. Recompila ate 3x

Isso e feito no arquivo _processed (temporario), NAO no fonte original.

---

## 5. Flags de Compilacao GnuCOBOL

| Flag | Funcao |
|------|--------|
| -w | Suprime warnings |
| -frelax-syntax-checks | Permite variantes de sintaxe (ex: posicao de REDEFINES) |
| -frelax-level-hierarchy | Permite niveis numericos nao-correspondentes |
| -flarger-redefines-ok | Permite REDEFINES maior que o original |
| -I cobol_build/copy | Diretorio de copybooks |

---

## 6. Resultado da Compilacao

| Status | Quantidade | Percentual |
|--------|-----------|-----------|
| Compila com sucesso | 26 | 62% |
| Falha (mapas CICS duplicados) | 5 | 12% |
| Falha (REDEFINES posicional) | 6 | 14% |
| Falha (IF desbalanceado) | 5 | 12% |

### Programas que compilam:
FGAA004, FGAA005, FGAA007, FGAA012D, FGAA015, FGAA032D, FGAA050D, FGAA115D,
FGAT030D, FGEV006D, OGEV020D, OGEV430D, OGEV431D, OGEV432D, OGEV434D,
OGEV435D, OGEV436D, OGEV441D, OGEV442D, OGEV444D, OGEV445D, OGEV446D,
OGEV535D, OGEV680D, OGEV690D, OGEV720D

---

## 7. Diferencas de Comportamento Detectadas

Ao comparar a execucao do programa Original vs Convertido (PF-GAA-L004 / FGAA004):

| Placa | Original (v6.1 - 2026) | Convertido (v4.1 - 2024) | Motivo |
|-------|------------------------|--------------------------|--------|
| ABC1D23 | 11 (Mercosul SP) | 12 (Mercosul Outros) | Faixa UDA-UGV/UOG-USB adicionada em 2025 |
| BFA5B67 | 12 (Mercosul Outros) | 11 (Mercosul SP) | Range BFA-GKI tratado diferente |
| ABC1234 | 21 (Antiga SP) | 21 (Antiga SP) | Igual |
| AB12345 | 33 (2 letras Carros) | 33 (2 letras Carros) | Igual |

O Original tem patches de 2025/2026 (ranges UDA-UGV, UOG-USB, TIO-TMJ).
O Convertido e versao 4.1 de Set/2024 que nao tem esses patches.
