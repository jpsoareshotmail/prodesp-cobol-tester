# Atividades Praticas - CRUD com PostgreSQL

**Objetivo:** aprender os fundamentos de banco de dados relacional praticando
operacoes CRUD (Create, Read, Update, Delete) em PostgreSQL.

---

## Preparacao do ambiente

Antes de comecar, deixe o ambiente pronto:

1. **Instalar o PostgreSQL** (versao 14 ou superior)
   - Windows: baixar em https://www.postgresql.org/download/windows/
   - Ou usar Docker: `docker run --name pg-estudo -e POSTGRES_PASSWORD=estudo123 -p 5432:5432 -d postgres:16`

2. **Instalar um cliente SQL** para escrever as consultas (escolha um):
   - pgAdmin (vem com o instalador do PostgreSQL)
   - DBeaver (gratuito, multiplataforma)
   - Extensao SQL do VS Code

3. **Criar o banco de estudo:**
   ```sql
   CREATE DATABASE loja_estudo;
   ```

4. **Rodar o script inicial:** execute o arquivo `schema.sql` (nesta mesma pasta)
   para criar as tabelas e os dados de exemplo.

> Dica: sempre teste cada comando no cliente SQL e observe o resultado antes de
> passar para o proximo.

---

## Modelo de dados (o que voce vai usar)

Uma pequena loja com duas tabelas:

- **categoria** (id, nome)
- **produto** (id, nome, preco, quantidade_estoque, categoria_id)

Um produto pertence a uma categoria (relacao 1-para-muitos).

---

## Modulo 1 - Conhecendo o banco (READ)

Objetivo: aprender a consultar dados com SELECT.

### Atividades
1.1. Liste todos os produtos cadastrados.
1.2. Liste apenas o nome e o preco de todos os produtos.
1.3. Liste os produtos com preco maior que R$ 50,00.
1.4. Liste os produtos ordenados do mais caro para o mais barato.
1.5. Conte quantos produtos existem no total.
1.6. Liste os produtos cujo nome comeca com a letra "C".

### Conceitos praticados
`SELECT`, `WHERE`, `ORDER BY`, `COUNT`, `LIKE`.

---

## Modulo 2 - Cadastrando dados (CREATE)

Objetivo: aprender a inserir novos registros com INSERT.

### Atividades
2.1. Cadastre uma nova categoria chamada "Bebidas".
2.2. Cadastre um novo produto na categoria "Bebidas" (escolha nome, preco e estoque).
2.3. Cadastre 3 produtos de uma vez so (INSERT com varias linhas).
2.4. Tente cadastrar um produto sem informar o nome. O que acontece? Por que?
2.5. Tente cadastrar um produto com categoria_id que nao existe. O que acontece?

### Conceitos praticados
`INSERT INTO`, `VALUES`, `NOT NULL`, chave estrangeira (foreign key).

---

## Modulo 3 - Atualizando dados (UPDATE)

Objetivo: aprender a alterar registros existentes com UPDATE.

### Atividades
3.1. Aumente em 10% o preco de todos os produtos.
3.2. Altere o estoque de um produto especifico para 100.
3.3. Renomeie a categoria "Bebidas" para "Bebidas e Sucos".
3.4. **Cuidado:** rode um UPDATE **sem** WHERE e observe quantas linhas mudam.
     (Faca isso apenas para aprender; depois rode o `schema.sql` de novo para restaurar.)

### Conceitos praticados
`UPDATE`, `SET`, importancia do `WHERE`.

---

## Modulo 4 - Removendo dados (DELETE)

Objetivo: aprender a excluir registros com DELETE.

### Atividades
4.1. Exclua um produto especifico pelo id.
4.2. Exclua todos os produtos com estoque igual a zero.
4.3. Tente excluir uma categoria que ainda tem produtos. O que acontece? Por que?
4.4. Explique a diferenca entre `DELETE` e `TRUNCATE`.

### Conceitos praticados
`DELETE`, `WHERE`, restricao de integridade referencial.

---

## Modulo 5 - Relacionamentos (JOIN)

Objetivo: consultar dados de duas tabelas ao mesmo tempo.

### Atividades
5.1. Liste cada produto com o **nome da sua categoria** (em vez do id).
5.2. Liste quantos produtos existem em cada categoria.
5.3. Liste as categorias que **nao tem nenhum produto** (dica: LEFT JOIN).
5.4. Liste o produto mais caro de cada categoria.

### Conceitos praticados
`INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `MAX`, `HAVING`.

---

## Modulo 6 - Desafio final (montar do zero)

Objetivo: aplicar tudo criando uma nova estrutura sozinho.

### Atividade
Crie uma tabela nova chamada **cliente** (id, nome, email, data_cadastro) e uma
tabela **pedido** que relacione um cliente a um produto, com quantidade e data.
Depois:

6.1. Escreva a DDL (CREATE TABLE) das duas tabelas, com chaves e constraints.
6.2. Cadastre 2 clientes e 3 pedidos.
6.3. Liste todos os pedidos com o nome do cliente e o nome do produto.
6.4. Calcule o valor total de cada pedido (quantidade x preco do produto).
6.5. Liste o cliente que mais gastou.

### Conceitos praticados
Modelagem, `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, JOIN de 3 tabelas, agregacao.

---

## Como entregar

Para cada modulo, o estagiario deve entregar:
- Um arquivo `.sql` com os comandos de cada atividade (comentados com o numero da atividade).
- Um breve texto respondendo as perguntas conceituais (2.4, 2.5, 3.4, 4.3, 4.4).

Sugestao de organizacao dos arquivos de resposta:
```
respostas/
  modulo1.sql
  modulo2.sql
  ...
  modulo6.sql
  conceitos.md
```

---

## Criterios de avaliacao

| Criterio | O que observar |
|----------|----------------|
| Correcao | Os comandos retornam o resultado esperado |
| Uso de WHERE | UPDATE e DELETE sempre com filtro adequado |
| Legibilidade | Comandos formatados e comentados |
| Entendimento | Respostas conceituais corretas |
| Modelagem (mod. 6) | Chaves e relacionamentos bem definidos |

---

## Dicas de boas praticas (leia antes de comecar)

1. **Sempre teste um SELECT antes de um UPDATE/DELETE** com o mesmo WHERE, para ver
   quais linhas serao afetadas.
2. **Nunca rode UPDATE ou DELETE sem WHERE** em producao (aqui e so estudo).
3. Use nomes de tabela e coluna em minusculo e sem acento.
4. Termine todo comando SQL com ponto e virgula `;`.
5. Comente seu codigo: `-- isto e um comentario em SQL`.

Bom estudo!
