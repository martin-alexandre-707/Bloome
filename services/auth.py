from config import criar_conexao

def login (usuario: str, senha : str ):
    try:
        con= criar_conexao()
        cursor= con.cursor()
        cursor.execute("SELECT * FROM usuarios where email=%s and password=%s", (usuario, senha))
        return cursor.fetchone()
    except Exception as e:
        print(e)