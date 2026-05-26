from config.db import criar_conexao


def insert_acessorio(nome: str, categoria: str, valor_venda: float, insumos: list):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            INSERT INTO acessorios (nome_acessorios, categoria_acessorio, valor_acessorio)
            VALUES (%s, %s, %s)
            ON CONFLICT (nome_acessorios) DO NOTHING
            RETURNING id_acessorios
        """, (nome, categoria, valor_venda))

        resultado = cursor.fetchone()

        if resultado is None:
            print(f"Produto '{nome}' já existe. Use a opção 3 para atualizar.")
            con.rollback()
            return

        id_acessorio = resultado[0]

        for nome_insumo, quantidade in insumos:
            cursor.execute("SELECT id_insumos FROM insumos WHERE nome = %s", (nome_insumo,))
            insumo_encontrado = cursor.fetchone()
            
            if not insumo_encontrado:
                print(f"Aviso: Insumo '{nome_insumo}' não encontrado. Este insumo não foi vinculado.")
                continue
                
            id_insumo = insumo_encontrado[0]
            
            cursor.execute("""
                INSERT INTO composicao_acessorios (id_insumos, id_acessorios, quantidade)
                VALUES (%s, %s, %s)
            """, (id_insumo, id_acessorio, quantidade))

        con.commit()
        print(f"Produto '{nome}' cadastrado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao cadastrar '{nome}': {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def listar_acessorios(nome=None):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        if not nome:
            cursor.execute("""
                SELECT id_acessorios, nome_acessorios, categoria_acessorio, valor_acessorio
                  FROM acessorios
            """)
        else:
            cursor.execute("""
                SELECT id_acessorios, nome_acessorios, categoria_acessorio, valor_acessorio
                  FROM acessorios
                 WHERE nome_acessorios ILIKE %s
            """, (f"%{nome}%",))

        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def listar_composicao(nome_acessorio: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            SELECT i.nome, ca.quantidade, i.valor_unitario,
                   (ca.quantidade * i.valor_unitario) AS subtotal
              FROM composicao_acessorios ca
              JOIN insumos i ON i.id_insumos = ca.id_insumos
              JOIN acessorios a ON a.id_acessorios = ca.id_acessorios
             WHERE a.nome_acessorios = %s
        """, (nome_acessorio,))

        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar composição: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def calcular_custo_insumos(nome_acessorio: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(ca.quantidade * i.valor_unitario), 0)
              FROM composicao_acessorios ca
              JOIN insumos i ON i.id_insumos = ca.id_insumos
              JOIN acessorios a ON a.id_acessorios = ca.id_acessorios
             WHERE a.nome_acessorios = %s
        """, (nome_acessorio,))

        return float(cursor.fetchone()[0])

    except Exception as e:
        print(f"Erro ao calcular custo: {e}")
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def deletar_acessorio(nome: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            DELETE FROM acessorios
             WHERE nome_acessorios = %s
        """, (nome,))

        con.commit()

        if cursor.rowcount == 0:
            print(f"Produto '{nome}' não encontrado.")
        else:
            print(f"Produto '{nome}' deletado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()

        # Aqui está o truque: verificamos se o erro é por causa de vínculo com vendas
        erro_str = str(e).lower()
        if "foreign key" in erro_str:
            print(f"\nErro: Não é possível excluir '{nome}'.")
            print("Este produto já possui histórico de vendas e não pode ser removido.")
            print("Para fins de auditoria, mantenha o produto registrado.")
        else:
            print(f"Erro ao excluir '{nome}': {e}")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def atualizar_acessorio(nome: str, novo_nome: str, categoria: str, valor_venda: float):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            UPDATE acessorios
               SET nome_acessorios     = %s,
                   categoria_acessorio = %s,
                   valor_acessorio     = %s
             WHERE nome_acessorios = %s
        """, (novo_nome, categoria, valor_venda, nome))

        con.commit()

        if cursor.rowcount == 0:
            print(f"Produto '{nome}' não encontrado.")
        else:
            print(f"Produto '{nome}' atualizado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao atualizar '{nome}': {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
