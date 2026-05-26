from repositories.insumos import insert_insumos, listar_insumos, deletar_insumos, atualizar_insumos, insumo_possui_dependencias
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
                print("\n--- Insumos Cadastrados ---")
                todos = listar_insumos()
                if not todos:
                    print("Nenhum insumo cadastrado.")
                    pausar()
                    continue
                for i in todos:
                    print(f"  {i[0]:<4} | {i[1]}")
                print("-" * 30)

                try:
                    nome = input("Nome do insumo que deseja atualizar: ").strip().lower()

                    insumos_existentes = listar_insumos(nome)
                    insumo_encontrado = None
                    for i in insumos_existentes:
                        if i[1] == nome:
                            insumo_encontrado = i
                            break

                    if not insumo_encontrado:
                        print(f"Insumo '{nome}' não encontrado no sistema.")
                        pausar()
                        continue

                    print(f"\nDados atuais:")
                    print(f"  Nome     : {insumo_encontrado[1]}")
                    print(f"  Valor    : R$ {float(insumo_encontrado[2]):.2f}")
                    print(f"  Estoque  : {float(insumo_encontrado[3])}")
                    print(f"  Categoria: {insumo_encontrado[4]}")
                    print("\nNovos dados (Enter para manter o atual):")

                    novo_nome = input(f"Nome [{insumo_encontrado[1]}]: ").strip().lower() or insumo_encontrado[1]
                    valor_str = input(f"Valor unitário [{float(insumo_encontrado[2]):.2f}]: ").replace(",", ".")
                    valor = float(valor_str) if valor_str else float(insumo_encontrado[2])
                    qtd_str = input(f"Quantidade em estoque [{float(insumo_encontrado[3])}]: ").replace(",", ".")
                    quantidade = float(qtd_str) if qtd_str else float(insumo_encontrado[3])
                    categoria = input(f"Categoria [{insumo_encontrado[4]}]: ").strip().lower() or insumo_encontrado[4]

                    atualizar_insumos(nome, novo_nome, valor, quantidade, categoria)
                except ValueError:
                    print("Erro: valor e quantidade devem ser números.")
                pausar()

            case "4":
                print("\n--- Insumos Cadastrados ---")
                todos = listar_insumos()
                if not todos:
                    print("Nenhum insumo cadastrado.")
                    pausar()
                    continue
                for i in todos:
                    print(f"  {i[0]:<4} | {i[1]}")
                print("-" * 30)

                nome = input("Nome do insumo que deseja deletar: ").strip().lower()

                insumos_existentes = listar_insumos(nome)
                insumo_encontrado = any(i[1] == nome for i in insumos_existentes)

                if not insumo_encontrado:
                    print(f"Insumo '{nome}' não encontrado no sistema.")
                else:
                    confirmacao = input(f"Tem certeza que deseja deletar '{nome}'? (S/N): ").strip().upper()
                    if confirmacao == "S":
                        if insumo_possui_dependencias(nome):
                            print(f"\nAviso: '{nome}' está na composição de um ou mais produto(s).")
                            print("Removê-lo irá desvincular esses produtos dos seus materiais.")
                            confirmacao_extra = input("Deseja continuar mesmo assim? (S/N): ").strip().upper()
                            if confirmacao_extra != "S":
                                print("Abortado.")
                                pausar()
                                continue

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
