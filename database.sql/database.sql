-- ============================================================
--  BLOOME - Script de criação do banco de dados
-- ============================================================

-- TABELAS
-- ============================================================

CREATE TABLE usuarios (
    id_usuarios SERIAL PRIMARY KEY,
    usuario     VARCHAR(255) UNIQUE NOT NULL,
    senha       BYTEA NOT NULL
);

CREATE TABLE insumos (
    id_insumos         SERIAL PRIMARY KEY,
    nome               VARCHAR(255) UNIQUE NOT NULL,
    valor_unitario     DECIMAL(10, 2) NOT NULL CHECK (valor_unitario >= 0),
    quantidade_estoque DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    categoria          VARCHAR(255) NOT NULL
);

CREATE TABLE acessorios (
    id_acessorios       SERIAL PRIMARY KEY,
    nome_acessorios     VARCHAR(225) UNIQUE NOT NULL,
    categoria_acessorio VARCHAR(225),
    valor_acessorio     DECIMAL(10, 2) NOT NULL CHECK (valor_acessorio >= 0)
);

CREATE TABLE composicao_acessorios (
    id_insumos    INTEGER NOT NULL REFERENCES insumos(id_insumos) ON DELETE CASCADE,
    id_acessorios INTEGER NOT NULL REFERENCES acessorios(id_acessorios) ON DELETE CASCADE,
    quantidade    DECIMAL(10, 2) NOT NULL CHECK (quantidade > 0),
    PRIMARY KEY (id_insumos, id_acessorios)
);

CREATE TABLE pedidos (
    id_pedidos          SERIAL PRIMARY KEY,
    data_pedidos        DATE DEFAULT CURRENT_DATE,
    metodo_de_pagamento VARCHAR(255) NOT NULL CHECK (metodo_de_pagamento IN ('Pix', 'Dinheiro', 'Cartão')),
    nome_cliente        VARCHAR(255),
    valor_total         DECIMAL(10, 2) DEFAULT 0 CHECK (valor_total >= 0)
);

CREATE TABLE despesas (
    id_despesas   SERIAL PRIMARY KEY,
    descricao     VARCHAR(255) NOT NULL,
    valor         DECIMAL(10, 2) NOT NULL CHECK (valor > 0),
    data_despesas DATE DEFAULT CURRENT_DATE,
    categoria     VARCHAR(255) NOT NULL
);

CREATE TABLE itens_pedidos (
    id_pedidos         INTEGER NOT NULL REFERENCES pedidos(id_pedidos) ON DELETE CASCADE,
    id_acessorios      INTEGER NOT NULL REFERENCES acessorios(id_acessorios),
    quantidade_vendida INTEGER NOT NULL CHECK (quantidade_vendida > 0),
    valor_unitario     DECIMAL(10, 2) NOT NULL CHECK (valor_unitario >= 0),
    PRIMARY KEY (id_pedidos, id_acessorios)
);

-- FUNÇÕES E TRIGGERS
-- ============================================================

-- Baixa o estoque dos insumos ao registrar uma venda
CREATE OR REPLACE FUNCTION baixar_estoque()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE insumos
    SET quantidade_estoque = quantidade_estoque - (ca.quantidade * NEW.quantidade_vendida)
    FROM composicao_acessorios ca
    WHERE ca.id_acessorios = NEW.id_acessorios
      AND insumos.id_insumos = ca.id_insumos;

    IF EXISTS (
        SELECT 1 FROM insumos i
        JOIN composicao_acessorios ca ON ca.id_insumos = i.id_insumos
        WHERE ca.id_acessorios = NEW.id_acessorios
          AND i.quantidade_estoque < 0
    ) THEN
        RAISE EXCEPTION 'insumos_quantidade_estoque_check: Estoque insuficiente para o acessório %', NEW.id_acessorios;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_baixar_estoque
AFTER INSERT ON itens_pedidos
FOR EACH ROW
EXECUTE FUNCTION baixar_estoque();


-- Devolve o estoque dos insumos ao deletar um item de venda
CREATE OR REPLACE FUNCTION devolver_estoque()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE insumos
    SET quantidade_estoque = quantidade_estoque + (ca.quantidade * OLD.quantidade_vendida)
    FROM composicao_acessorios ca
    WHERE ca.id_acessorios = OLD.id_acessorios
      AND insumos.id_insumos = ca.id_insumos;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_devolver_estoque
AFTER DELETE ON itens_pedidos
FOR EACH ROW
EXECUTE FUNCTION devolver_estoque();


-- VIEWS
-- ============================================================

CREATE OR REPLACE VIEW resumo_pedidos AS
SELECT
    p.id_pedidos,
    p.data_pedidos,
    p.metodo_de_pagamento,
    p.nome_cliente,
    ac.nome_acessorios           AS produto,
    ip.quantidade_vendida,
    ip.valor_unitario,
    (ip.quantidade_vendida * ip.valor_unitario) AS subtotal
FROM pedidos p
JOIN itens_pedidos ip ON p.id_pedidos     = ip.id_pedidos
JOIN acessorios    ac ON ip.id_acessorios = ac.id_acessorios;