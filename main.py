from config.db import criar_conexao
from repositories.insumos import insert_insumos

nome = input("Digite o nome do insumo: ").strip
valor_unitario = input("Digite o valor unitario do insumo: ")
quantidade_estoque = input("Digite a quantidade do estoque:  ")
categoria = input("Digite a categoria: ")
insert_insumos(nome, valor_unitario, quantidade_estoque, categoria)
