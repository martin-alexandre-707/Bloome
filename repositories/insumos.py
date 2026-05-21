from config.db import criar_conexao

def insert_insumos(nome :str, valor_unitario: float, quantidade_estoque: float, categoria : str):
  
    try:
        con = criar_conexao()
        cursor = con.cursor()

        cursor.execute("INSERT INTO insumos (nome, valor_unitario, quantidade_estoque, categoria) VALUES (%s, %s, %s, %s)", (nome, valor_unitario, 
        quantidade_estoque, categoria))

        con.commit()
        print(f"Insumo '{nome}' cadastrado com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
    finally: 
        cursor.close()
        con.close()

