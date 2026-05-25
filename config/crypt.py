import bcrypt

def criptografar(senha):
    password_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed

def checar_password(senha, hashed):
    password_bytes = senha.encode('utf-8')
    return bcrypt.checkpw(password_bytes, bytes(hashed))