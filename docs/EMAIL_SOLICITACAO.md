# Email de Solicitacao

---

**Para:** TI / Infraestrutura BRQ
**CC:** Gestao do Projeto Prodesp
**Assunto:** Solicitacao de ambiente para testes COBOL - Projeto Prodesp

---

Prezados,

Para dar continuidade aos testes de validacao da migracao COBOL do projeto Prodesp, precisamos dos seguintes itens:

---

## 1. Acesso Administrador (maquina local)

Necessario para instalar o compilador COBOL comercial (Rocket Visual COBOL Personal Edition — gratuito).

**Acao:** Liberar acesso admin temporario na maquina do usuario `jennersoares`, ou instalar remotamente:
- Visual Studio 2022 Community
- Rocket Visual COBOL for Visual Studio Personal Edition 11.0

---

## 2. Instancia DB2

Necessario para executar e validar as queries SQL dos programas convertidos.

**Opcoes:**

| Opcao | Descricao | Custo |
|-------|-----------|-------|
| A | DB2 Community Edition em Docker (local ou EC2) | Gratis |
| B | Amazon RDS for Db2 | ~$50/mes |
| C | IBM Db2 on Cloud | Free tier |

**O que precisamos receber:**
- Host, porta, usuario e senha de acesso
- DDL das tabelas (CREATE TABLE) ou acesso ao schema
- Amostra de dados de teste para as 30+ tabelas utilizadas pelos programas

---

## 3. Copybooks originais

Sao os arquivos de definicao de campos (COPY libraries) do ambiente Unisys/Micro Focus.

**O que precisamos:** conteudo dos ~200 copybooks (WSD01002, WSD01118, WSD01073, WSD12012, WSFUR001, WSFUR022, WSTAB002, WSTAB057, entre outros).

**Formato:** arquivos texto (.cpy ou .cbl), podem ser extraidos da biblioteca de COPY do mainframe/servidor.

---

## 4. Liberacao de porta na EC2

Necessario para disponibilizar o painel de testes para acesso da equipe.

**Acao:** Liberar inbound TCP porta 5000 no Security Group da instancia EC2 `44.195.132.167`.

---

Fico a disposicao para alinhamento.

Atenciosamente,
Jenner Soares
Equipe BRQ - Projeto Prodesp
