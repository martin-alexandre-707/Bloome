from config.db import criar_conexao


def buscar_acessorio_por_nome(nome: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            SELECT id_acessorios, nome_acessorios, valor_acessorio
              FROM acessorios
             WHERE nome_acessorios = %s
        """, (nome,)) 

        acessorio = cursor.fetchone()
        return acessorio

    except Exception as e:
        print(f"Erro ao buscar acessório '{nome}': {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def inserir_pedido(nome_cliente: str, metodo_de_pagamento: str, valor_total: float, carrinho: list):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            INSERT INTO pedidos (nome_cliente, metodo_de_pagamento, valor_total)
            VALUES (%s, %s, %s)
            RETURNING id_pedidos
        """, (nome_cliente, metodo_de_pagamento, valor_total))

        resultado = cursor.fetchone()
        id_pedido = resultado[0]

        for item in carrinho:
            id_acessorio = item[0]
            quantidade   = item[2]
            valor_unitario = item[3]

            cursor.execute("""
                INSERT INTO itens_pedidos (id_pedidos, id_acessorios, quantidade_vendida, valor_unitario)
                VALUES (%s, %s, %s, %s)
            """, (id_pedido, id_acessorio, quantidade, valor_unitario))

        con.commit()
        print(f"\nVenda registrada com sucesso! ID do Pedido: #{id_pedido}")

    except Exception as e:
        if con:
            con.rollback()
            
        mensagem_erro = str(e)
        
        
        if "insumos_quantidade_estoque_check" in mensagem_erro:
            print("\n VENDA CANCELADA: Estoque de insumos insuficiente para fabricar as peças!")
            print("Vá no 'Menu de Insumos' e reabasteça o estoque dos materiais.")
        else:
            
            print(f"\n Erro ao registrar a venda: {e}")
            
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def listar_historico_vendas():
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            SELECT id_pedidos, data_pedidos, nome_cliente, metodo_de_pagamento, valor_total
              FROM pedidos
             ORDER BY data_pedidos DESC, id_pedidos DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao buscar o histórico de vendas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def gerar_relatorio_financeiro():
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        # Conta quantos pedidos existem e soma a coluna valor_total
        cursor.execute("""
            SELECT COUNT(id_pedidos), COALESCE(SUM(valor_total), 0)
              FROM pedidos
        """)
        
        resultado = cursor.fetchone()
        total_vendas = resultado[0]
        faturamento_total = resultado[1]

        return total_vendas, faturamento_total

    except Exception as e:
        print(f"Erro ao gerar o financeiro: {e}")
        return 0, 0.0
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def verificar_estoque_carrinho(carrinho: list) -> list:
    """Retorna lista de problemas de estoque antes de gravar a venda."""
    con = None
    cursor = None
    problemas = []
    consumo_por_insumo = {}
    try:
        con = criar_conexao()
        cursor = con.cursor()

        for item in carrinho:
            id_acessorio, nome_produto, quantidade, _ = item

            cursor.execute("""
                SELECT i.id_insumos,
                       i.nome,
                       ca.quantidade * %s AS necessario
                  FROM composicao_acessorios ca
                  JOIN insumos i ON i.id_insumos = ca.id_insumos
                 WHERE ca.id_acessorios = %s
            """, (quantidade, id_acessorio))

            for ins in cursor.fetchall():
                id_insumo = ins[0]
                if id_insumo not in consumo_por_insumo:
                    consumo_por_insumo[id_insumo] = {
                        'produtos'  : [],
                        'insumo'    : ins[1],
                        'necessario': 0.0
                    }

                if nome_produto not in consumo_por_insumo[id_insumo]['produtos']:
                    consumo_por_insumo[id_insumo]['produtos'].append(nome_produto)

                consumo_por_insumo[id_insumo]['necessario'] += float(ins[2])

        for id_insumo, dados in consumo_por_insumo.items():
            cursor.execute("""
                SELECT quantidade_estoque
                  FROM insumos
                 WHERE id_insumos = %s
            """, (id_insumo,))

            resultado = cursor.fetchone()
            if not resultado:
                continue

            disponivel = float(resultado[0])
            necessario = dados['necessario']

            if disponivel < necessario:
                problemas.append({
                    'produto'   : ", ".join(dados['produtos']),
                    'insumo'    : dados['insumo'],
                    'disponivel': disponivel,
                    'necessario': necessario
                })

        return problemas

    except Exception as e:
        print(f"Erro ao verificar estoque: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
