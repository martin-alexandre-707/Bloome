from repositories.acessorios import (
    insert_acessorio, listar_acessorios, listar_composicao,
    calcular_custo_insumos, deletar_acessorio, atualizar_acessorio
)
from repositories.insumos import listar_insumos
from config.utils import limpar_tela, pausar


def _selecionar_insumos():
    insumos_disponiveis = listar_insumos()

    if not insumos_disponiveis:
        print("Nenhum insumo cadastrado. Cadastre insumos antes de criar um produto.")
        return None

    print("\n--- Insumos Disponíveis ---")
    for insumo in insumos_disponiveis:
        print(f"- {insumo[1]:<20} | R$ {float(insumo[2]):.2f} | Estoque: {float(insumo[3])}")

    insumos_selecionados = []
    custo_total = 0.0

    print("\nAdicione os insumos do produto (Deixe vazio e aperte Enter para finalizar):")

    while True:
        nome_digitado = input("Nome do insumo: ").strip().lower()

        if nome_digitado == "":
            if len(insumos_selecionados) == 0:
                print("Você precisa adicionar ao menos um insumo.")
                continue  
            else:
                break     

        if not nome_digitado.replace(" ","").isalpha():
            print("Erro: O nome do insumo deve conter apenas letras.")
            continue

        insumo_encontrado = None
        
        for item in insumos_disponiveis:
            nome_do_item = item[1]
            if nome_do_item.lower() == nome_digitado:
                insumo_encontrado = item
                break 

        if insumo_encontrado is None:
            print("Insumo não encontrado. Tente novamente.")
            continue

        while True:
            try:
                quantidade = float(input(f"Quantidade de '{insumo_encontrado[1]}': ").replace(",", "."))
                if quantidade <= 0:
                    print("A quantidade deve ser maior que zero.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Digite apenas números para a quantidade.")

        valor_unitario = float(insumo_encontrado[2])
        subtotal = quantidade * valor_unitario
        custo_total = custo_total + subtotal

        insumos_selecionados.append((insumo_encontrado[1], quantidade))

        print(f"  + Adicionado: {quantidade}x {insumo_encontrado[1]} | Custo acumulado: R$ {custo_total:.2f}")

    return insumos_selecionados, custo_total


def menu_acessorios():
    while True:
        limpar_tela()
        print("\n" + "="*30)
        print("       GERENCIAR ACESSORIOS")
        print("="*30)
        print("1 - Cadastrar Produto")
        print("2 - Listar Produtos")
        print("3 - Atualizar Produto")
        print("4 - Deletar Produto")
        print("0 - Voltar")
        print("="*30)

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                try:
                    while True:
                        nome = input("Nome do produto: ").strip().lower()
                        if nome != "" and nome.replace(" ","").isalpha():
                            break
                        print("Erro: O nome do produto deve conter apenas letras.")

                    while True:
                        categoria = input("Categoria: ").strip().lower()
                        if categoria != "" and categoria.replace(" ","").isalpha():
                            break
                        print("Erro: A categoria deve conter apenas letras.")

                    resultado = _selecionar_insumos()
                    if resultado is None:
                        pausar()
                        continue

                    insumos_selecionados, custo_insumos = resultado

                    print(f"\nCusto total de insumos: R$ {custo_insumos:.2f}")
                    valor_venda = float(input("Preço de venda (R$): ").replace(",", "."))
                    lucro = valor_venda - custo_insumos

                    print(f"\n--- Resumo ---")
                    print(f"Custo de insumos : R$ {custo_insumos:.2f}")
                    print(f"Preço de venda   : R$ {valor_venda:.2f}")
                    print(f"Lucro estimado   : R$ {lucro:.2f}")

                    confirmar = input("\nConfirmar cadastro? (S/N): ").strip().upper()
                    if confirmar == "S":
                        insert_acessorio(nome, categoria, valor_venda, insumos_selecionados)
                    else:
                        print("Cancelado.")
                except ValueError:
                    print("Erro: preço de venda deve ser um número.")
                pausar()

            case "2":
                while True:
                    busca = input("Digite o nome para buscar (ou pressione Enter para listar todos): ").strip().lower()
                    if busca == "" or busca.replace(" ","").isalpha():
                        break
                    print("Erro: O nome para buscar deve conter apenas letras.")

                busca = busca or None
                produtos = listar_acessorios(busca)

                if produtos:
                    print("\n--- Lista de Produtos ---")
                    for produto in produtos:
                        nome_produto = produto[1]
                        custo = calcular_custo_insumos(nome_produto)
                        lucro = float(produto[3]) - custo
                        print(f"{produto[0]:<4} | {nome_produto:<25} | {produto[2]:<15} | Venda: R$ {float(produto[3]):<8.2f} | Custo: R$ {custo:<8.2f} | Lucro: R$ {lucro:.2f}")
                else:
                    if busca:
                        print(f"Nenhum produto encontrado com o nome '{busca}'.")
                    else:
                        print("Nenhum produto cadastrado no sistema.")
                pausar()

            case "3":
                print("\n--- Produtos Cadastrados ---")
                todos = listar_acessorios()
                if not todos:
                    print("Nenhum produto cadastrado.")
                    pausar()
                    continue
                for p in todos:
                    print(f"  {p[0]:<4} | {p[1]}")
                print("-" * 30)

                try:
                    while True:
                        nome = input("Nome do produto que deseja atualizar: ").strip().lower()
                        if nome != "" and nome.replace(" ","").isalpha():
                            break
                        print("Erro: O nome do produto deve conter apenas letras.")

                    produtos_existentes = listar_acessorios(nome)
                    produto_encontrado = None
                    if produtos_existentes:
                        for produto in produtos_existentes:
                            if produto[1] == nome:
                                produto_encontrado = produto
                                break

                    if not produto_encontrado:
                        print(f"Produto '{nome}' não encontrado no sistema.")
                        pausar()
                        continue

                    print(f"\nDados atuais:")
                    print(f"  Nome     : {produto_encontrado[1]}")
                    print(f"  Categoria: {produto_encontrado[2]}")
                    print(f"  Valor    : R$ {float(produto_encontrado[3]):.2f}")
                    print("\nNovos dados (Enter para manter o atual):")

                    while True:
                        novo_nome = input(f"Nome [{produto_encontrado[1]}]: ").strip().lower()
                        if novo_nome == "":
                            novo_nome = produto_encontrado[1]
                            break
                        if novo_nome.replace(" ","").isalpha():
                            break
                        print("Erro: O nome do produto deve conter apenas letras.")

                    while True:
                        categoria = input(f"Categoria [{produto_encontrado[2]}]: ").strip().lower()
                        if categoria == "":
                            categoria = produto_encontrado[2]
                            break
                        if categoria.replace(" ","").isalpha():
                            break
                        print("Erro: A categoria deve conter apenas letras.")

                    valor_str = input(f"Preço de venda [{float(produto_encontrado[3]):.2f}]: ").replace(",", ".")
                    valor_venda = float(valor_str) if valor_str else float(produto_encontrado[3])

                    atualizar_acessorio(nome, novo_nome, categoria, valor_venda)

                except ValueError:
                    print("Erro: preço de venda deve ser um número.")
                pausar()

            case "4":
                print("\n--- Produtos Cadastrados ---")
                todos = listar_acessorios()
                if not todos:
                    print("Nenhum produto cadastrado.")
                    pausar()
                    continue
                for p in todos:
                    print(f"  {p[0]:<4} | {p[1]}")
                print("-" * 30)

                while True:
                    nome = input("Nome do produto que deseja deletar: ").strip().lower()
                    if nome != "" and nome.replace(" ","").isalpha():
                        break
                    print("Erro: O nome do produto deve conter apenas letras.")

                produtos_existentes = listar_acessorios(nome)
                produto_encontrado = False
                
                if produtos_existentes:
                    for produto in produtos_existentes:
                        if produto[1] == nome:
                            produto_encontrado = True
                            break
                
                if produto_encontrado:
                    confirmacao = input(f"Tem certeza que deseja deletar '{nome}'? (S/N): ").strip().upper()
                    if confirmacao == "S":
                        deletar_acessorio(nome)
                    else:
                        print("Abortado. O produto foi mantido.")
                
                else:

                    print(f"Produto '{nome}' não encontrado no sistema. Não é possível deletar.")
                    
                pausar()

            case "0":
                print("Voltando ao menu principal...")
                break

            case _:
                print("Opção inválida, tente novamente.")
                pausar()
