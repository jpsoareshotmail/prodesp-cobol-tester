# E-mail: Solicitação de pendências — Migração COBOL Unisys → z/OS COBOL 6.5/DB2

**Para:** [destinatário Prodesp]
**De:** [seu nome]
**Assunto:** Migração COBOL — solicitação de itens pendentes (copybooks, DDL/DB2, CSD)

---

Prezados,

Na validação dos 42 programas convertidos, 26 já compilam e executam (62%). Os 16 restantes, e a validação completa dos demais, dependem dos itens abaixo. Solicitamos o envio:

## 1. Copybooks completos (PDS)

PDS completo de copybooks (equivalente a `SYS1.COPYLIB`) dos programas abaixo — os stubs que geramos localmente não cobrem todos os campos usados nos fontes:

`FGAT006D`, `OGAA013D`, `OGAA018D`, `OGAA255D`, `OGAA615D`, `OGAA640D`, `OGAA792D`, `OGAA920D`, `OGEV005D`, `OGEV021D`, `OGEV630D`, `OGEV635D`, `PGAA100D`

## 2. DDL das tabelas + instância DB2

- DDL (`CREATE TABLE`) de todas as tabelas DB2/DMS usadas pelos 42 programas
- Uma instância DB2 (LUW local ou z/OS de homologação) com esse schema provisionado
- Massa de dados de teste (ou aval para gerarmos massa sintética)

Hoje o `EXEC SQL` é comentado para compilar no GnuCOBOL — sem banco real, o acesso a dados não é validado, nem nos 26 programas que já compilam.

## 3. Definições CICS (CSD)

CSD com as definições de transação/programa dos 42 programas — hoje o `EXEC CICS` está stubado.

## 4. Confirmação: patches de faixa de placas 2025/2026

5 diferenças de faixa entre original e convertido. Aplicar no convertido antes ou depois da migração?

---

Itens 1 e 4 destravam os 16 programas pendentes. Itens 2 e 3 são necessários para validar comportamento, não só compilação. Disponíveis para call se ajudar a agilizar.

Atenciosamente,
[nome]
