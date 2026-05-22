from config.db import criar_conexao

def login (usuario: str, senha : str ):
    try:
        con= criar_conexao()
        cursor= con.cursor()
        cursor.execute("SELECT * FROM usuarios where usuario=%s and senha=%s", (usuario, senha))
        return cursor.fetchone()
    except Exception as e:
        print(e)