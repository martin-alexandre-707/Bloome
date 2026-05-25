import getpass
import os
from config.crypt import criptografar, checar_password
from repositories.auth import login, cadastrar_usuario
from services.insumos_service import menu_insumos


def menu_principal():
    while True:
        print("\n" + "="*30)
        print("         MENU PRINCIPAL")
        print("="*30)
        print("1 - Gerenciar Insumos")
        # print("2 - Produtos")   ← só adicionar aqui
        print("0 - Sair")
        print("="*30)

        match input("Opção: "):
            case "1": menu_insumos()
            case "0": print("Até logo!")
            break
            case _: print("Opção inválida.")


def autenticar():
    print("1 - Login\n2 - Cadastrar usuário")
    match input("Escolha: "):
        case "1":
            usuario = input("Usuário: ")
            senha = getpass.getpass("Senha: ")
            user = login(usuario)

            if user and checar_password(senha, user[1]):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Seja bem-vindo, {usuario}!")
                menu_principal()
            else:
                print("Usuário ou senha inválidos.")

        case "2":
            usuario = input("Usuário: ")
            senha = getpass.getpass("Senha: ")
            cadastrar_usuario(usuario, criptografar(senha))

        case _:
            print("Opção inválida.")


autenticar()
