# Plano de Teste - Primeiro Emplacamento (Original + Melhorias)

Documento comparativo entre o **roteiro original** entregue pela Prodesp
(`Roteiros de Teste/*.docx`) e a **versao revisada/melhorada**, formalizada como
roteiro de teste executavel.

- **Origem:** 3 documentos Word - cenarios Capital, Interior/Litoral e Orgao Oficial.
- **Objetivo do processo:** primeiro emplacamento de veiculo zero-km.
- **Data da revisao:** julho/2026.

---

## 1. Cenarios e dados de teste

| Cenario | Categoria | Chassi | Identificador do proprietario |
|---------|-----------|--------|-------------------------------|
| Capital | Particular | 9C2GAA1SNSP772009 | CPF 09758787861 |
| Interior/Litoral | Particular | 9BMGAA1SNSP772016 | CPF 81742145850 |
| Orgao Oficial | Oficial | 9C2GAA1SNSP772010 | CNPJ 08518623000162 |

---

## 2. Roteiro ORIGINAL (transcricao fiel dos documentos)

Transcricao do fluxo descrito nos `.docx`, na ordem em que aparece.
Cenario particular (Capital / Interior-Litoral):

1. Para realizar o primeiro emplacamento de um veiculo-zero, o chassi deve existir na base fabril do Serpro. Informa-se o chassi.
2. O chassi esta sem emplacamento na BIN/Serpro. A consulta executou a transacao **901** da BIN - consulta veiculo por chassi. Ao clicar "Enter" retorna a tela para informar um parametro de pesquisa.
3. Para o primeiro emplacamento de veiculo com categoria diferente de oficial, deve existir uma taxa com codigo de pagamento 06. A taxa e enviada pela SEFAZ e recebida no sistema pela transacao **RAUT**, window WDGAA35, ou, em caso excepcional, pelo programa batch de contingencia **GAA/B100/DB**.
4. Execucao da transacao RAUT para inclusao da taxa de codigo de pagamento 06 com o CPF.
5. Consulta da taxa - **TXUT**. O CPF tem apenas a taxa acima; clicando "Enter", a transacao solicita um parametro de pesquisa.
6. Para iniciar o processo, cria-se uma ficha de primeiro emplacamento no **eCRV** (ou outro canal). Escolha de placa dentre as placas selecionadas gratuitamente. Preenche-se a ficha. Ao clicar "ENVIAR", gera-se a ficha no mainframe.
7. A consulta da ficha no mainframe - **PGER**. Com "Enter", retorna-se a tela de parametros.
8. Para processar a ficha, ela precisa passar por uma avaliacao, e isto ocorre no eCRV. Ao clicar "SALVAR", aprova-se a ficha, e altera-se a situacao da ficha no mainframe de **1 para 5** - **PGER**.
9. Processamento da ficha no mainframe. Antes, uma vez por dia, deve-se executar **DHAB**. Inicio do processamento.
10. Na proxima tela aparece a mensagem de placa cadastrada no Detran (**PEPM**) e na base fabril da BIN (**PTRE**), e as opcoes da solicitacao de autorizacao de estampagem.
11. Com a atualizacao da base fabril pela transacao da BIN, a base ampliada fica com pendencia de emissao de CRV; e obrigatorio executar a transacao **EDUT**.
12. Consulta da base ampliada (**CDAV**), destacando a pendencia de emissao de CRV. Emissao do CRV. Processo concluido com sucesso.
13. Consultas do cadastro da placa: base estadual **PEPM**, BIN, base fabril **PTRE**, base ampliada **CDAV**.
14. Eliminando a pendencia de emplacamento: requer colaboracao de empresa de TI que atue no sistema EMPLACA (ambiente dev/homologacao). Na ausencia dessa parceria, a alternativa e cancelar a solicitacao de autorizacao de estampagem - consulta **PEST**, cancelamento **CEST**.

**Diferencas do cenario Orgao Oficial:**
- Para veiculo de categoria oficial, **nao existe taxa** com codigo de pagamento 06 (passos 3-5 nao se aplicam).
- O CNPJ deve estar no cadastro de CNPJ oficial - transacao **PJOF**. Consulta-se o CNPJ; nao existindo, deve-se inserir o CNPJ no cadastro.

---

## 3. Analise critica do roteiro original

Pontos fortes:
- Descreve o fluxo ponta a ponta e cita as transacoes reais do mainframe.
- Traz dados de teste concretos (chassi, CPF, CNPJ) por cenario.
- Cobre o caminho de excecao (cancelamento de estampagem).

Lacunas identificadas (o que impede de ser um roteiro de teste executavel):
1. **Sem resultado esperado por passo** - descreve o que acontece, mas nao formaliza o criterio de aprovacao/reprovacao.
2. **Sem pre-condicoes explicitas** - ex.: taxa previamente recebida, base fabril carregada.
3. **Mistura de camadas** - acoes do eCRV (aplicacao) e consultas do mainframe (transacoes) aparecem juntas, dificultando saber "o que testar onde".
4. **Dependencia externa nao isolada** - o passo de estampagem depende do sistema EMPLACA (terceiro), sem alternativa de teste automatizada.
5. **Sem rastreabilidade para os programas COBOL** - nao liga cada passo ao programa/fonte correspondente.

---

## 4. Roteiro REVISADO (melhorado, formato executavel)

Cada passo agora tem: acao, camada (eCRV/mainframe/externo), transacao, e
**resultado esperado**. Cenario particular:

| # | Acao | Camada | Transacao | Resultado esperado |
|---|------|--------|-----------|--------------------|
| 1 | Consultar chassi na BIN/Serpro | Externo (BIN) | 901 | Chassi existe na base fabril e retorna "sem emplacamento" |
| 2 | Incluir taxa cod. pagamento 06 (SEFAZ) | Mainframe | RAUT / GAA-B100-DB | Taxa 06 registrada e vinculada ao CPF |
| 3 | Consultar taxa | Mainframe | TXUT | Exibe a taxa 06 do CPF |
| 4 | Criar ficha (escolher placa gratuita, preencher, ENVIAR) | eCRV | - | Ficha gerada no mainframe com situacao = 1 |
| 5 | Consultar ficha | Mainframe | PGER | Ficha existe com situacao = 1 |
| 6 | Aprovar ficha (SALVAR) | eCRV | - | Aprovacao registrada |
| 7 | Confirmar mudanca de situacao | Mainframe | PGER | Situacao da ficha muda de 1 para 5 |
| 8 | Executar processamento diario | Mainframe | DHAB | Processamento do emplacamento iniciado |
| 9 | Verificar cadastro da placa e estampagem | Mainframe | PEPM / PTRE | Placa cadastrada no Detran (PEPM) e base fabril (PTRE); opcoes de estampagem exibidas |
| 10 | Emitir CRV | Mainframe | EDUT | Pendencia de emissao de CRV eliminada; CRV emitido |
| 11 | Consultar base ampliada | Mainframe | CDAV | Base ampliada sem pendencia; emplacamento concluido |
| 12 | Consultar cadastro completo | Mainframe | PEPM/BIN/PTRE/CDAV | Placa presente e consistente nas quatro bases |
| E1 | (Excecao) Cancelar estampagem | Externo/Mainframe | PEST / CEST | Solicitacao de estampagem cancelada |

**Passos exclusivos do Orgao Oficial** (substituem os passos 2-3 de taxa):

| # | Acao | Camada | Transacao | Resultado esperado |
|---|------|--------|-----------|--------------------|
| 2o | Verificar CNPJ no cadastro oficial | Mainframe | PJOF | CNPJ oficial encontrado (ou inserido, se ausente) |

Observacao: categoria oficial e isenta de taxa 06, portanto os passos de taxa
(RAUT/TXUT) nao se aplicam.

---

## 5. Melhorias aplicadas em relacao ao original

1. **Resultado esperado por passo** - transforma a descricao em criterio verificavel.
2. **Separacao por camada** - deixa claro o que e acao no eCRV, transacao no mainframe ou dependencia externa.
3. **Correcao de fidelidade** - a aprovacao da ficha (SALVAR) e acao do eCRV; a mudanca de situacao 1->5 e o que se confirma via PGER (antes estavam fundidos num unico passo).
4. **Passo de excecao isolado (E1)** - o cancelamento de estampagem vira caminho alternativo explicito.
5. **Renumeracao limpa do fluxo oficial** - sem passos fracionados.
6. **Rastreabilidade COBOL** - ver secao 6.

---

## 6. Rastreabilidade: transacao -> programa COBOL

| Transacao | Descricao | Programa COBOL (amostragem) |
|-----------|-----------|------------------------------|
| 901 | Consulta veiculo por chassi | Sistema externo (BIN/Serpro) |
| RAUT | Inclusao de taxa (SEFAZ) | - (window WDGAA35) |
| GAA/B100/DB | Batch de contingencia da taxa | **PGAA100D** (PF-GAA-B100-DB) - compila no ambiente |
| TXUT | Consulta de taxa | - |
| PGER | Consulta/situacao da ficha | - |
| DHAB | Processamento diario | - |
| PEPM | Cadastro da placa (Detran) | - |
| PTRE | Base fabril da BIN | - |
| EDUT | Emissao de CRV | - |
| CDAV | Base ampliada da BIN | - |
| PJOF | Cadastro de CNPJ oficial | - |
| PEST | Consulta de estampagem | - |
| CEST | Cancelamento de estampagem | - |

**Nota:** apenas `GAA/B100/DB` tem correspondencia direta e confirmada com um
programa da amostragem recebida (`PGAA100D`). As demais transacoes pertencem a
sistemas externos (BIN/Serpro, eCRV) ou a programas ainda nao presentes na
amostragem - o que reforca a necessidade dos fontes/copybooks pendentes para
uma validacao ponta a ponta.

---

## 7. Analise dos prints de tela (imagens dos documentos)

Os `.docx` contem 40-44 prints de tela por cenario. Analisando as capturas,
foi possivel confirmar as telas reais e extrair dados que o texto nao trazia:

**Ambiente:** Unisys ClearPath MCP acessado via Web Enabler
(host `HNPRDSP06`, IP `10.200.206.132`, window `WDMCS/1`).

**Telas confirmadas (cenario Capital):**

| Passo | Tela / Transacao | Dados observados no print |
|-------|------------------|---------------------------|
| Consulta chassi | **PER1** - Pesquisa de veiculos no RENAVAM | Chassi 9C2GAA1SNSP772009 informado; retorna sem emplacamento |
| Consulta taxa | **TXUT** - Pesquisa de taxas por CPF/CNPJ | CPF 097.587.878-61, COD.SERV 06, COD.PGTO 06, VALOR R$ 150,00, SITUACAO 0-Aguarda Uso |
| Criar ficha | **eCRV (web)** - Primeiro Registro de Veiculo | Categoria PARTICULAR, placa gratuita escolhida: DSR-0A30 (SP-Municipio) |
| Ficha gerada | Ficha PDF (fichaCadastral.do) | Ficha No 860/2025, proprietario ALESSANDRA ALMEIDA, RENAVAM |
| Cadastro/emplacamento | **CAV2** - Cadastro de Certificados / Primeiro Emplacamento | Placa DSR0A30, RENAVAM 01001057632, TIPO 04, CATEG 01 |
| Situacao da ficha | **PGE4/GEVER** - Situacao de registro em GEVERDS | Ficha 860/2025, OPCAO 01-Primeiro Emplacamento, **STATUS REG 05**, 01-Aprovado |
| Emissao CRV | **DUT1/EDUT** - Emissao do Documento Unico de Transito | Placa DSR0A30, tipo 1 (1a via) |
| Consulta ampliada | **CDAV** - Dados ampliados na RENAVAM | IND.CRV ELETR SIM, NUMERO CRV 250001955268, sem pendencia |

**Descobertas relevantes:**
1. O **eCRV e uma aplicacao web** moderna (nao mainframe) - a criacao da ficha e
   a escolha da placa acontecem no portal do Governo SP, so depois refletindo no mainframe.
2. O texto dizia "situacao muda de 1 para 5"; o print **confirma STATUS REG = 05** na
   tela GEVER, validando o campo real (dataset **GEVERDS**, que ja mapeamos na ferramenta de estrutura).
3. As telas mainframe usam codigos proprios (PER1, TXUT, CAV2, PGE4, DUT1, CDAV) alem
   das transacoes citadas no texto - util para rastrear a origem dos dados de teste.
4. Os dados de teste sao **consistentes e reais** (mesmo chassi/CPF/placa aparecem em
   todas as telas), servindo como massa de validacao confiavel.

---

## 8. Limitacoes e proximos passos

- **Estampagem depende do sistema EMPLACA** (terceiro) - nao ha como automatizar
  esse trecho sem o ambiente parceiro; o roteiro preve o cancelamento como
  alternativa de teste.
- **Validacao end-to-end** exige os programas/copybooks e o banco DB2 pendentes
  (ver `docs/EMAIL_SOLICITACAO_PRODESP.md` e `docs/analise/COPYBOOKS_FALTANTES.md`).
- Os roteiros estao disponiveis na aba **"Roteiros de Teste"** do dashboard.
- Os prints foram extraidos para analise; para incluir as imagens no dashboard,
  usar `scripts/analise/extrair_imgs_docx.py`.
