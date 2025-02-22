import streamlit as st
import styles  # Importa o novo módulo de estilos com os botões customizados
from auth import logout, authenticate
from patient import show_patient_dashboard
from professional import show_professional_dashboard
from database import login_user, register_user

# Inicializar variáveis no session_state, se não existirem
if 'menu' not in st.session_state:
    st.session_state.menu = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'patients' not in st.session_state:
    st.session_state.patients = {}
if 'professional_menu' not in st.session_state:
    st.session_state.professional_menu = None

def show_home():
    """Tela inicial com botões estilizados de Login e Cadastro."""
    with st.container():
        st.markdown("""
        <h1 style='text-align: center; margin-bottom: 5px;'>Academia Diagnóstica</h1>
        <h4 style='text-align: center; margin-bottom: 30px;'>Correções Automatizadas e Acompanhamento Longitudinal</h4>
        """, unsafe_allow_html=True)
    
    st.markdown(styles.get_css(), unsafe_allow_html=True)

    # Criando três colunas para melhor alinhamento dos botões
    left, middle, right = st.columns([1, 2, 1])

    with middle:  # Centralizando os botões na coluna do meio
        if st.button("Login", key="login_button", use_container_width=True):
            st.session_state.menu = "login"
            st.rerun()
        
        if st.button("Cadastro", key="cadastro_button", use_container_width=True):
            st.session_state.menu = "cadastro"
            st.rerun()

def show_login():
    """Tela de login."""
    st.subheader("Acesso ao Sistema")
    username = st.text_input("Nome de Usuário")
    password = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)  # Criando duas colunas para os botões ficarem lado a lado
    with col1:
        if st.button("Entrar", use_container_width=True):
            if username and password:
                authenticate(username, password)  # Agora autentica corretamente
            else:
                st.error("Preencha todos os campos.")

    with col2:
        if st.button("Voltar", use_container_width=True):
            st.session_state.menu = None
            st.rerun()

def show_register():
    """Tela de cadastro de usuário."""
    st.subheader("Criação de Conta")
    new_user = st.text_input("Nome de Usuário")
    new_password = st.text_input("Senha", type="password")
    role = st.selectbox("Selecione seu perfil", ["Paciente", "Profissional"], key="role_select")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registrar", key="register_button", use_container_width=True):
            if new_user and new_password:
                sucesso = register_user(new_user, new_password, role)
                if sucesso:
                    st.success("✅ Cadastro realizado com sucesso! Faça login.")
                    st.session_state.menu = "login"
                else:
                    st.error("⚠ Erro: Nome de usuário já existe ou ocorreu um problema no cadastro.")
            else:
                st.error("❌ Preencha todos os campos antes de registrar.")
    
    with col2:
        if st.button("Voltar", key="back_button_register", use_container_width=True):
            st.session_state.menu = None
            st.rerun()

def show_dashboard():
    """Tela do usuário autenticado."""
    st.success(f"Bem-vindo(a), {st.session_state.user}! Você está logado como {st.session_state.role}.")

    if st.session_state.role == "Profissional":
        show_professional_dashboard()
    else:
        st.subheader("Área exclusiva para Pacientes")
        show_patient_dashboard()
    
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.menu = None
        st.rerun()





