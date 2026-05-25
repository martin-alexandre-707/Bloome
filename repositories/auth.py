from config.db import criar_conexao


def login(usuario: str):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute(
            "SELECT usuario, senha FROM usuarios WHERE usuario = %s",
            (usuario,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def cadastrar_usuario(usuario: str, senha_hashed):
    con = None
    cursor = None
    try:
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)",
            (usuario, senha_hashed))
        con.commit()
        print("Usuário cadastrado com sucesso!")

    except Exception as e:
        if con:
            con.rollback()
            
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            print("Esse usuário já existe!")
        else:
            print(f"Erro ao cadastrar usuário: {e}")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()