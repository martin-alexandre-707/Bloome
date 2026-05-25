from config.db import criar_conexao


def login(usuario: str):
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
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def cadastrar_usuario(usuario: str, senha_hashed):
    try:
        con = criar_conexao()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)",
            (usuario, senha_hashed))
        con.commit()
        print("Usuário cadastrado com sucesso!")

    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Esse usuário já existe!")
        else:
            print(f"Erro ao cadastrar usuário: {e}")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()