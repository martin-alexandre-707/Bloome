# 🌸 Bloome — Sistema de Gestão de Vendas

Sistema de gestão interna para controle de insumos, produtos (acessórios) e vendas, desenvolvido em Python com banco de dados PostgreSQL.

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado e rodando
- Git

---

## 🚀 Como rodar do zero

### 1. Clone o repositório

```bash
git clone https://github.com/martin-alexandre-707/Bloome.git
cd Bloome
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

No PostgreSQL, crie um banco chamado `bloome` (ou o nome que preferir):

```sql
CREATE DATABASE bloome;
```

Depois execute o script de criação das tabelas:

```bash
psql -U postgres -d bloome -f database.sql
```

Ou abra o arquivo `database.sql` direto no pgAdmin e execute.

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Abra o `.env` e preencha com os dados do seu PostgreSQL:

```
DB_NAME=bloome
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### 6. Rode o sistema

```bash
python main.py
```

---

## 📁 Estrutura do projeto

```
Bloome/
├── config/
│   ├── crypt.py          # Criptografia de senhas (bcrypt)
│   ├── db.py             # Conexão com o PostgreSQL
│   └── utils.py          # Utilitários (limpar tela, pausar)
├── repositories/
│   ├── auth.py           # Login e cadastro de usuários
│   ├── acessorios.py     # CRUD de produtos
│   ├── insumos.py        # CRUD de insumos
│   └── pedidos.py        # Registro e histórico de vendas
├── services/
│   ├── cadastro_services.py  # Menu de produtos
│   ├── insumos_service.py    # Menu de insumos
│   └── vendas.py             # Menu de vendas
├── database.sql          # Script de criação do banco
├── main.py               # Ponto de entrada do sistema
├── requirements.txt      # Dependências Python
├── .env.example          # Exemplo de configuração
└── .gitignore
```

---

## 🗄️ Banco de dados

O arquivo `database.sql` cria automaticamente:

- Todas as tabelas do sistema
- Triggers para controle automático de estoque
- View de resumo de pedidos

---

## 📦 Dependências

| Pacote | Versão | Uso |
|---|---|---|
| bcrypt | 5.0.0 | Criptografia de senhas |
| psycopg2-binary | 2.9.12 | Conexão com PostgreSQL |
| python-dotenv | 1.2.2 | Variáveis de ambiente |
