from repositories.pedidos import buscar_acessorio_por_nome, inserir_pedido, listar_historico_vendas, gerar_relatorio_financeiro, verificar_estoque_carrinho
from repositories.acessorios import listar_acessorios
from config.utils import limpar_tela, pausar


def menu_vendas():
    while True:
        limpar_tela()
        print("\n" + "="*30)
        print("         MÓDULO DE VENDAS")
        print("="*30)
        print("1 - Registrar Nova Venda")
        print("2 - Histórico de Vendas")
        print("3 - Relatório Financeiro")  
        print("0 - Voltar")
        print("="*30)

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                registrar_venda()
                pausar()

            case "2":
                exibir_historico()
                pausar()

            case "3": 
                exibir_relatorio_financeiro()
                pausar()

            case "0":
                print("Voltando ao menu principal...")
                break

            case _:
                print("Opção inválida, tente novamente.")
                pausar()

def exibir_historico():
    limpar_tela()
    print("\n" + "="*55)
    print("                 HISTÓRICO DE VENDAS")
    print("="*55)
    
    vendas = listar_historico_vendas()
    
    if vendas:
        print(f"{'ID':<4} | {'Data':<10} | {'Cliente':<15} | {'Pgto':<10} | {'Total':>8}")
        print("-" * 55)
        for v in vendas:
            id_venda = v[0]
            data_venda = v[1].strftime("%d/%m/%Y") 
            cliente = v[2]
            pgto = v[3]
            total = float(v[4])
            
            print(f"#{id_venda:<3} | {data_venda:<10} | {cliente:<15} | {pgto:<10} | R$ {total:>6.2f}")
        print("-" * 55)
    else:
        print("\nNenhuma venda registrada até o momento.")


def _exibir_problemas_estoque(problemas):
    print("\nVENDA BLOQUEADA — Estoque insuficiente:")
    for p in problemas:
        print(f"  Produto '{p['produto']}' precisa de {p['necessario']:.2f} de '{p['insumo']}', mas só há {p['disponivel']:.2f} em estoque.")
    print("\nAbasteca o estoque antes de registrar esta venda.")


def registrar_venda():
    limpar_tela()
    print("\n" + "="*30)
    print("        NOVO PEDIDO")
    print("="*30)

    nome_cliente = input("Nome do cliente (ou Enter para pular): ").strip()

    if nome_cliente == "":
        nome_cliente = "Consumidor Final"

    produtos_cadastrados = listar_acessorios()
    print("\n--- Tabela de Preços (Produtos Disponíveis) ---")
    if produtos_cadastrados:
        for prod in produtos_cadastrados:
            print(f"- {prod[1]:<20} | R$ {float(prod[3]):.2f}")
    else:
        print("Nenhum produto cadastrado no banco de dados.")

    carrinho = []
    total_geral = 0.0

    print("\n--- Adicionar Produtos ao Carrinho ---")
    print("(Deixe o nome em branco e pressione Enter para finalizar)\n")

    while True:
        nome_produto = input("Nome do produto: ").strip().lower()

        if nome_produto == "":
            break 

        acessorio = buscar_acessorio_por_nome(nome_produto)

        if acessorio is None:
            print(f"Produto '{nome_produto}' não encontrado. Tente novamente.")
        else:
            # CORTE 1: Tiramos a variável estoque_atual
            id_acessorio, nome_encontrado, valor_unitario = acessorio[0], acessorio[1], float(acessorio[2])

            # CORTE 2: Tiramos o estoque do print
            print(f"Encontrado: {nome_encontrado} | Preço: R$ {valor_unitario:.2f}")

            while True:
                try:
                    quantidade = int(input("Quantidade desejada: "))
                    
                    # CORTE 3: Tiramos a barreira do estoque
                    if quantidade <= 0:
                        print("A quantidade deve ser maior que zero.")
                    else:
                        break 
                except ValueError:
                    print("Erro: digite apenas números inteiros.")

            subtotal = quantidade * valor_unitario
            total_geral += subtotal

            produto_ja_no_carrinho = False
            for indice, item in enumerate(carrinho):
                if item[0] == id_acessorio:
                    quantidade_atual = item[2]
                    carrinho[indice] = (item[0], item[1], quantidade_atual + quantidade, item[3])
                    produto_ja_no_carrinho = True
                    break

            if not produto_ja_no_carrinho:
                carrinho.append((id_acessorio, nome_encontrado, quantidade, valor_unitario))
            
            print(f"  + Adicionado! Subtotal: R$ {subtotal:.2f} | Carrinho: R$ {total_geral:.2f}\n")

    if len(carrinho) == 0:
        print("Nenhum produto foi adicionado. Operação cancelada.")
        return

    limpar_tela()
    print("\n" + "="*30)
    print("       RESUMO DO PEDIDO")
    print("="*30)
    print(f"Cliente: {nome_cliente}\n")
    print(f"{'Produto':<20} | {'Qtd':>4} | {'Unit.':>8} | {'Subtotal':>10}")
    print("-"*52)

    for item in carrinho:
        print(f"{item[1]:<20} | {item[2]:>4} | R$ {item[3]:>6.2f} | R$ {(item[2] * item[3]):>8.2f}")

    print("="*52)
    print(f"{'TOTAL GERAL':>38} R$ {total_geral:>8.2f}")
    print("="*52)

    problemas = verificar_estoque_carrinho(carrinho)
    if problemas:
        _exibir_problemas_estoque(problemas)
        return

    while True:
        print("\nMétodos: Pix | Dinheiro | Cartão")
        metodo_pagamento = input("Pagamento: ").strip().title() 

        if metodo_pagamento == "Pix" or metodo_pagamento == "Dinheiro" or metodo_pagamento == "Cartão":
            break 
        else:
            print("Opção inválida. Digite exatamente: Pix, Dinheiro ou Cartão.")

    confirmacao = input(f"\nConfirmar venda de R$ {total_geral:.2f}? (S/N): ").strip().upper()

    if confirmacao == "S":
        problemas = verificar_estoque_carrinho(carrinho)
        if problemas:
            _exibir_problemas_estoque(problemas)
        else:
            inserir_pedido(nome_cliente, metodo_pagamento, total_geral, carrinho)
    else:
        print("Venda cancelada.")

def exibir_relatorio_financeiro():
    limpar_tela()
    print("\n" + "="*40)
    print("  RELATÓRIO FINANCEIRO SIMPLES ")
    print("="*40)

    total_vendas, faturamento_total = gerar_relatorio_financeiro()

    print(f"Total de Vendas Realizadas : {total_vendas}")
    print(f"Faturamento Total da Loja  : R$ {float(faturamento_total):.2f}")
    
    if total_vendas > 0:
        ticket_medio = float(faturamento_total) / total_vendas
        print(f"Ticket Médio por Venda     : R$ {ticket_medio:.2f}")

    print("="*40)
