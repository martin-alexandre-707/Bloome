from config.db import criar_conexao


def insert_insumos(nome: str, valor_unitario: float, quantidade_estoque: float, categoria: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            INSERT INTO insumos (nome, valor_unitario, quantidade_estoque, categoria)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (nome) DO NOTHING
        """, (nome, valor_unitario, quantidade_estoque, categoria))

        con.commit()

        if cursor.rowcount == 0:
            print(f"Insumo '{nome}' já existe. Use a opção 3 para atualizar.")
        else:
            print(f"Insumo '{nome}' cadastrado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao inserir '{nome}': {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def listar_insumos(nome_insumo=None):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        if not nome_insumo:
            cursor.execute("""
                SELECT id_insumos, nome, valor_unitario, quantidade_estoque, categoria
                  FROM insumos
            """)
        else:
            cursor.execute("""
                SELECT id_insumos, nome, valor_unitario, quantidade_estoque, categoria
                  FROM insumos
                 WHERE nome ILIKE %s
            """, (f"%{nome_insumo}%",))

        insumos = cursor.fetchall()
        return insumos

    except Exception as e:
        print(f"Erro ao listar insumos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def insumo_possui_dependencias(nome: str) -> bool:
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM composicao_acessorios ca
                  JOIN insumos i ON i.id_insumos = ca.id_insumos
                 WHERE i.nome = %s
            )
        """, (nome,))

        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Erro ao verificar dependências do insumo '{nome}': {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def deletar_insumos(nome: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("DELETE FROM insumos WHERE nome = %s", (nome,))

        con.commit()

        if cursor.rowcount == 0:
            print(f"Insumo '{nome}' não encontrado.")
        else:
            print(f"'{nome}' deletado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao excluir {nome}: {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def atualizar_insumos(nome: str, novo_nome: str, valor_unitario: float, quantidade_estoque: float, categoria: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("""
            UPDATE insumos
               SET nome               = %s,
                   valor_unitario     = %s,
                   quantidade_estoque = %s,
                   categoria          = %s
             WHERE nome = %s
        """, (novo_nome, valor_unitario, quantidade_estoque, categoria, nome))

        con.commit()

        if cursor.rowcount == 0:
            print(f"Insumo '{nome}' não encontrado.")
        else:
            print(f"Insumo '{nome}' atualizado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
        print(f"Erro ao atualizar '{nome}': {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
