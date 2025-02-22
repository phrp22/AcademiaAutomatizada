import streamlit as st
import styles  
import psycopg2
from ui import show_home, show_login, show_register, show_dashboard
from database import create_db
from auth import authenticate, logout  # Certifique-se de que auth.py contém essas funções corretamente

# Criar banco de dados apenas UMA VEZ ao iniciar
if 'db_initialized' not in st.session_state:
    create_db()
    st.session_state.db_initialized = True

# Adiciona o CSS do styles.py
st.markdown(styles.get_css(), unsafe_allow_html=True)

# Inicializar session_state
if 'menu' not in st.session_state:
    st.session_state.menu = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Definir qual tela exibir
if st.session_state.user is None:
    if st.session_state.menu == "login":
        show_login()
    elif st.session_state.menu == "cadastro":
        show_register()
    else:
        show_home()
else:
    show_dashboard()