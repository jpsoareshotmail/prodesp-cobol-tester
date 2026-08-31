-- =====================================================================
-- GABARITO - Atividades CRUD PostgreSQL
-- Uso do instrutor: referencia para corrigir as entregas do estagiario.
-- Pode haver mais de uma resposta correta para o mesmo exercicio.
-- =====================================================================

-- ============ MODULO 1 - READ ============
-- 1.1
SELECT * FROM produto;
-- 1.2
SELECT nome, preco FROM produto;
-- 1.3
SELECT * FROM produto WHERE preco > 50.00;
-- 1.4
SELECT * FROM produto ORDER BY preco DESC;
-- 1.5
SELECT COUNT(*) FROM produto;
-- 1.6
SELECT * FROM produto WHERE nome LIKE 'C%';

-- ============ MODULO 2 - CREATE ============
-- 2.1
INSERT INTO categoria (nome) VALUES ('Bebidas');
-- 2.2 (assumindo que Bebidas ficou com id 4; ajustar conforme o banco)
INSERT INTO produto (nome, preco, quantidade_estoque, categoria_id)
VALUES ('Suco de laranja 1L', 9.90, 35, (SELECT id FROM categoria WHERE nome='Bebidas'));
-- 2.3
INSERT INTO produto (nome, preco, quantidade_estoque, categoria_id) VALUES
    ('Refrigerante 2L', 8.00, 40, (SELECT id FROM categoria WHERE nome='Bebidas')),
    ('Agua mineral 500ml', 2.50, 200, (SELECT id FROM categoria WHERE nome='Bebidas')),
    ('Cha gelado 1L', 6.90, 25, (SELECT id FROM categoria WHERE nome='Bebidas'));
-- 2.4  Erro: coluna nome tem NOT NULL -> "null value in column nome violates not-null constraint"
-- 2.5  Erro: viola a foreign key -> "insert on table produto violates foreign key constraint"

-- ============ MODULO 3 - UPDATE ============
-- 3.1
UPDATE produto SET preco = preco * 1.10;
-- 3.2
UPDATE produto SET quantidade_estoque = 100 WHERE id = 1;
-- 3.3
UPDATE categoria SET nome = 'Bebidas e Sucos' WHERE nome = 'Bebidas';
-- 3.4  Sem WHERE, o UPDATE altera TODAS as linhas da tabela (por isso o cuidado).

-- ============ MODULO 4 - DELETE ============
-- 4.1
DELETE FROM produto WHERE id = 4;
-- 4.2
DELETE FROM produto WHERE quantidade_estoque = 0;
-- 4.3  Erro: a categoria e referenciada por produtos (FK) -> "violates foreign key constraint".
--      Solucao: excluir/reatribuir os produtos antes, ou usar ON DELETE CASCADE no modelo.
-- 4.4  DELETE remove linha a linha e aceita WHERE (pode ser desfeito em transacao);
--      TRUNCATE esvazia a tabela inteira de forma rapida, sem WHERE, e reseta contadores.

-- ============ MODULO 5 - JOIN ============
-- 5.1
SELECT p.nome AS produto, c.nome AS categoria
FROM produto p
JOIN categoria c ON p.categoria_id = c.id;
-- 5.2
SELECT c.nome, COUNT(p.id) AS total_produtos
FROM categoria c
LEFT JOIN produto p ON p.categoria_id = c.id
GROUP BY c.nome;
-- 5.3
SELECT c.nome
FROM categoria c
LEFT JOIN produto p ON p.categoria_id = c.id
WHERE p.id IS NULL;
-- 5.4
SELECT c.nome AS categoria, MAX(p.preco) AS preco_mais_alto
FROM categoria c
JOIN produto p ON p.categoria_id = c.id
GROUP BY c.nome;

-- ============ MODULO 6 - DESAFIO ============
-- 6.1
CREATE TABLE cliente (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE pedido (
    id          SERIAL PRIMARY KEY,
    cliente_id  INTEGER NOT NULL REFERENCES cliente(id),
    produto_id  INTEGER NOT NULL REFERENCES produto(id),
    quantidade  INTEGER NOT NULL CHECK (quantidade > 0),
    data_pedido DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 6.2
INSERT INTO cliente (nome, email) VALUES
    ('Maria Souza', 'maria@email.com'),
    ('Joao Lima',   'joao@email.com');

INSERT INTO pedido (cliente_id, produto_id, quantidade) VALUES
    (1, 1, 2),
    (1, 8, 1),
    (2, 9, 3);

-- 6.3
SELECT ped.id, cli.nome AS cliente, pro.nome AS produto, ped.quantidade
FROM pedido ped
JOIN cliente cli ON ped.cliente_id = cli.id
JOIN produto pro ON ped.produto_id = pro.id;

-- 6.4
SELECT ped.id, cli.nome AS cliente, pro.nome AS produto,
       ped.quantidade, pro.preco,
       (ped.quantidade * pro.preco) AS valor_total
FROM pedido ped
JOIN cliente cli ON ped.cliente_id = cli.id
JOIN produto pro ON ped.produto_id = pro.id;

-- 6.5
SELECT cli.nome, SUM(ped.quantidade * pro.preco) AS total_gasto
FROM pedido ped
JOIN cliente cli ON ped.cliente_id = cli.id
JOIN produto pro ON ped.produto_id = pro.id
GROUP BY cli.nome
ORDER BY total_gasto DESC
LIMIT 1;
