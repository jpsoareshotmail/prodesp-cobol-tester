# Roteiros de Teste - Primeiro Emplacamento

Analise dos documentos em `Roteiros de Teste/*.docx` (Prodesp). Descrevem o
processo funcional de primeiro emplacamento de veiculo zero-km, em tres cenarios.

## Cenarios e dados de teste

| Cenario | Categoria | Chassi | Identificador |
|---------|-----------|--------|---------------|
| Capital | Particular | 9C2GAA1SNSP772009 | CPF 09758787861 |
| Interior/Litoral | Particular | 9BMGAA1SNSP772016 | CPF 81742145850 |
| Orgao Oficial | Oficial | 9C2GAA1SNSP772010 | CNPJ 08518623000162 |

## Fluxo (particular - capital / interior-litoral)

1. Verificar chassi na base fabril do Serpro / sem emplacamento na BIN -> transacao **901**
2. Incluir taxa codigo de pagamento 06 (SEFAZ) -> **RAUT** (window WDGAA35) ou batch **GAA/B100/DB**
3. Consultar taxa -> **TXUT**
4. Criar ficha de emplacamento no eCRV (escolha de placa gratuita, preencher, ENVIAR)
5. Consultar ficha no mainframe -> **PGER**
6. Aprovar ficha no eCRV (SALVAR) -> situacao muda de 1 para 5 (**PGER**)
7. Processar -> **DHAB** (uma vez por dia)
8. Autorizacao de estampagem: placa cadastrada no Detran (**PEPM**) e base fabril (**PTRE**)
9. Emissao de CRV -> **EDUT**
10. Consultar cadastro: PEPM (estadual), BIN, PTRE (fabril), CDAV (ampliada)
11. Fallback: consultar estampagem (**PEST**) e cancelar (**CEST**)

## Diferencas do cenario Orgao Oficial

- **Sem taxa codigo 06** (categoria oficial e isenta) - passos 2 e 3 nao se aplicam
- Exige **CNPJ no cadastro de CNPJ oficial** -> transacao **PJOF**; se nao existir, inserir

## Transacoes x Programas COBOL

| Transacao | Descricao | Programa COBOL |
|-----------|-----------|----------------|
| 901 | Consulta veiculo por chassi (BIN/Serpro) | (externo - BIN) |
| RAUT | Inclusao de taxa (SEFAZ), window WDGAA35 | - |
| GAA/B100/DB | Batch de contingencia - recebimento de taxa | **PGAA100D** (PF-GAA-B100-DB) |
| TXUT | Consulta de taxa | - |
| PGER | Consulta/situacao da ficha | - |
| DHAB | Processamento diario | - |
| PEPM | Cadastro da placa (base estadual Detran) | - |
| PTRE | Base fabril da BIN | - |
| EDUT | Emissao de CRV | - |
| CDAV | Consulta da base ampliada BIN | - |
| PJOF | Cadastro de CNPJ oficial | - |
| PEST | Consulta de estampagem | - |
| CEST | Cancelamento de estampagem | - |

**Observacao:** o mapeamento transacao -> programa esta parcialmente identificado.
`GAA/B100/DB` corresponde diretamente ao programa `PGAA100D` (fonte `PF-GAA-B100-DB`)
que ja compila no ambiente. As demais transacoes sao de sistemas externos (BIN/Serpro,
eCRV) ou de programas ainda nao mapeados na amostragem recebida.

## Uso no dashboard

Os roteiros estao disponiveis na aba **"Roteiros de Teste"** do dashboard web,
com o passo a passo de cada cenario e a legenda das transacoes. Os dados de teste
(chassi, CPF, CNPJ) podem ser usados para alimentar os testes dos programas.
