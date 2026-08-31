-- =====================================================================
-- Script inicial - Loja de Estudo (CRUD PostgreSQL)
-- Rode este arquivo no banco loja_estudo antes de comecar as atividades.
-- Ele cria as tabelas e insere dados de exemplo.
-- Pode rodar quantas vezes quiser: ele apaga e recria tudo do zero.
-- =====================================================================

-- Remove as tabelas se ja existirem (ordem importa por causa da FK)
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS categoria;

-- ---------------------------------------------------------------------
-- Tabela: categoria
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    id      SERIAL PRIMARY KEY,          -- id auto-incremento
    nome    VARCHAR(50) NOT NULL UNIQUE  -- nome obrigatorio e unico
);

-- ---------------------------------------------------------------------
-- Tabela: produto
-- ---------------------------------------------------------------------
CREATE TABLE produto (
    id                  SERIAL PRIMARY KEY,
    nome                VARCHAR(100) NOT NULL,
    preco               NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
    quantidade_estoque  INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    categoria_id        INTEGER NOT NULL REFERENCES categoria(id)
);

-- ---------------------------------------------------------------------
-- Dados de exemplo
-- ---------------------------------------------------------------------
INSERT INTO categoria (nome) VALUES
    ('Alimentos'),
    ('Limpeza'),
    ('Eletronicos');

-- categoria_id: 1=Alimentos, 2=Limpeza, 3=Eletronicos
INSERT INTO produto (nome, preco, quantidade_estoque, categoria_id) VALUES
    ('Arroz 5kg',           28.90,  40, 1),
    ('Feijao 1kg',          8.50,   60, 1),
    ('Cafe 500g',           18.00,  25, 1),
    ('Chocolate',           6.75,   0,  1),
    ('Detergente',          2.99,  120, 2),
    ('Sabao em po 1kg',     14.50,  30, 2),
    ('Agua sanitaria 2L',   7.20,   0,  2),
    ('Fone de ouvido',      89.90,  15, 3),
    ('Carregador USB-C',    45.00,  50, 3),
    ('Cabo HDMI',           32.00,  22, 3);

-- ---------------------------------------------------------------------
-- Conferencia (opcional): descomente para ver os dados carregados
-- ---------------------------------------------------------------------
-- SELECT * FROM categoria;
-- SELECT * FROM produto;
