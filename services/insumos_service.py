from repositories.insumos import insert_insumos, listar_insumos, deletar_insumos, atualizar_insumos
from config.utils import limpar_tela, pausar


def menu_insumos():
    while True:
        limpar_tela()
        print("\n" + "="*30)
        print("       GERENCIAR INSUMOS")
        print("="*30)
        print("1 - Cadastrar Insumo")
        print("2 - Listar Insumos")
        print("3 - Atualizar Insumo")
        print("4 - Deletar Insumo")
        print("0 - Voltar")
        print("="*30)

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                try:
                    nome = input("Nome do insumo: ").strip().lower()
                    valor = float(input("Valor unitário: ").replace(",", "."))
                    quantidade = float(input("Quantidade em estoque: ").replace(",", "."))
                    categoria = input("Categoria: ").strip().lower()
                    insert_insumos(nome, valor, quantidade, categoria)
                except ValueError:
                    print("Erro: valor e quantidade devem ser números.")
                pausar()

            case "2":
                busca = input("Digite o nome para buscar (ou pressione Enter para listar todos): ").strip().lower()
                busca = busca or None
                insumos = listar_insumos(busca)

                if insumos:
                    print("\n--- Lista de Insumos ---")
                    for insumo in insumos:
                        print(f"{insumo[0]:<4} | {insumo[1]:<20} | R$ {float(insumo[2]):<8.2f} | Estoque: {float(insumo[3]):<8} | {insumo[4]}")
                else:
                    if busca:
                        print(f"Nenhum insumo encontrado com o nome '{busca}'.")
                    else:
                        print("Nenhum insumo cadastrado no sistema.")
                pausar()

            case "3":
                try:
                    nome = input(
                        "Nome do insumo que deseja atualizar: ").strip().lower()
                    novo_nome = input("Nome: ").strip().lower()
                    valor = float(input("Valor unitário: ").replace(",", "."))
                    quantidade = float(input("Quantidade em estoque: ").replace(",", "."))
                    categoria = input("Categoria: ").strip().lower()
                    atualizar_insumos(nome, novo_nome, valor,
                                      quantidade, categoria)
                except ValueError:
                    print("Erro: valor e quantidade devem ser números.")
                pausar()

            case "4":
                nome = input(
                    "Nome do insumo que deseja deletar: ").strip().lower()
                confirmacao = input(
                    f"Tem certeza que deseja deletar '{nome}'? (S/N): ").strip().upper()
                if confirmacao == "S":
                    deletar_insumos(nome)
                else:
                    print("Abortado.")
                pausar()

            case "0":
                print("Voltando ao menu principal...")
                break

            case _:
                print("Opção inválida, tente novamente.")
                pausar()
