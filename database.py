import streamlit as st
import psycopg2
import os
import bcrypt

# Verifica se as variáveis foram carregadas corretamente
if "SUPABASE_DATABASE_URL" in st.secrets:
    DATABASE_URL = st.secrets["SUPABASE_DATABASE_URL"]
    
else:
    st.error("❌ ERRO: Variável 'SUPABASE_DATABASE_URL' não encontrada nos Secrets do Streamlit Cloud.")
    DATABASE_URL = None  # Define como None para evitar erro de NameError

if "SUPABASE_API_KEY" in st.secrets:
    SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]
else:
    st.error("❌ ERRO: Variável 'SUPABASE_API_KEY' não encontrada nos Secrets do Streamlit Cloud.")
    SUPABASE_API_KEY = None  # Define como None para evitar erro de NameError

def create_db():
    """Cria as tabelas do banco de dados se ainda não existirem."""
    conn = get_db_connection()
    
    if conn is None:
        print("❌ Erro: Não foi possível conectar ao banco de dados.")
        return
    
    try:
        with conn.cursor() as c:
            # Criar tabela de usuários
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL
                        )''')

            # Criar tabela de respostas de escalas
            c.execute('''CREATE TABLE IF NOT EXISTS scale_responses (
                            id SERIAL PRIMARY KEY,
                            username TEXT NOT NULL,
                            scale_name TEXT NOT NULL,
                            responses TEXT NOT NULL,
                            timestamp TIMESTAMP DEFAULT NOW(),
                            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                        )''')

            conn.commit()
            print("✅ Banco de dados inicializado corretamente!")
    except psycopg2.Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("🔌 Conexão fechada corretamente após criação das tabelas.")

# Função para conectar ao banco de dados
def get_db_connection():
    """Cria uma conexão com o banco de dados Supabase."""
    if DATABASE_URL is None:
        st.error("❌ Erro: Conexão ao banco de dados não configurada.")
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except psycopg2.Error as e:
        st.error(f"❌ Erro ao conectar ao banco: {e}")
        return None

@st.cache_data(ttl=60)
def login_user(username, password):
    """Autentica o usuário verificando a senha e retorna o papel (role) corretamente."""
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT password, role FROM users WHERE username = %s", (username,))
            user_data = c.fetchone()
    except psycopg2.Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()

    if user_data:
        hashed_password, role = user_data
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            print(f"Login bem-sucedido! Usuário {username} autenticado como {role}.")
            return role
        else:
            print("Senha incorreta.")
    else:
        print("Usuário não encontrado.")
    return None

def register_user(username, password, role):
    """Registra um novo usuário no banco de dados com senha criptografada."""
    conn = get_db_connection()

    if conn is None:
        print("❌ Erro: Não foi possível conectar ao banco de dados.")
        return False  # Se a conexão falhar, não tenta registrar
    
    try:
        with conn.cursor() as c:
            # Verifica se o usuário já existe antes de tentar cadastrar
            c.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = c.fetchone()

            if existing_user:
                print("⚠ Erro: Nome de usuário já cadastrado.")
                return False  # Evita erro de duplicação

            # Criptografar a senha
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

            # Inserir novo usuário
            c.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING id",
                (username, hashed_pw, role)
            )
            user_id = c.fetchone()
            conn.commit()
        
        if user_id:
            print(f"✅ Usuário {username} cadastrado com sucesso! ID: {user_id[0]}")
            return True
        else:
            print(f"⚠ Erro: Usuário {username} pode não ter sido salvo corretamente.")
            return False

    except psycopg2.IntegrityError:
        conn.rollback()
        print("❌ Erro: O nome de usuário já existe.")
        return False
    except psycopg2.Error as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False
    finally:
        if conn:
            conn.close()  # Garante que a conexão seja fechada corretamente


@st.cache_data(ttl=60)
def get_user_role(username):
    """Retorna o papel do usuário (Paciente ou Profissional), armazenando em cache."""
    conn = get_db_connection()
    if conn is None:
        return None  # Evita erro ao tentar acessar cursor de conexão inexistente

    try:
        with conn.cursor() as c:
            c.execute("SELECT role FROM users WHERE username = %s", (username,))
            user_data = c.fetchone()
            return user_data[0] if user_data else None
    except psycopg2.Error as e:
        print(f"Erro ao buscar papel do usuário: {e}")
        return None
    finally:
        conn.close()


def save_scale_responses(username, scale_name, responses):
    """Salva as respostas da escala no banco de dados."""
    conn = get_db_connection()
    
    if conn is None:
        print("❌ Erro: Não foi possível conectar ao banco de dados.")
        return False
    
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO scale_responses (username, scale_name, responses) VALUES (%s, %s, %s)",
                (username, scale_name, str(responses))  # Convertendo lista para string antes de salvar
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"❌ Erro ao salvar respostas: {e}")
        return False
    finally:
        if conn:
            conn.close()