from config.db import criar_conexao
from repositories.insumos import insert_insumos
from repositories.auth import login 
import os

usuario=input("Digite o usuario: ")
password= input("Digite a sua senha: ")
user_logged = login(usuario, password)

# Aba insumos
#   Cadastrar novo insumo, colocando o nome (UNICO e com limite de 255 caractareses que nem o banco de dados), o valor unitario (pode ser >= 0 mas nn pode ser negativo) (metro ou unidade), quantidade a ser adicionada, e categoria que é o insumo ex: cordão, fecho e pingente.
#
# Ver estoque (select * from insumos)
#       
#
# Editar estoque
#   adicionar ou remover quantidade de insumo já existente
#
#
#
#



if user_logged:
    print("Seja bem-vindo!")
    while True:
        print("----MENU----/n1-Cadastrar insumos  /n2-")    
        opcao= input("Digite a opção que deseja acessar")
        match opcao:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
else:
    print("Usuário ou senha inválidos")