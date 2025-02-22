import streamlit as st
from database import login_user

def authenticate(username, password):
    """Autentica um usuário e armazena suas credenciais na sessão."""
    role = login_user(username, password)
    if role:
        st.session_state.user = username
        st.session_state.role = role
        st.session_state.menu = "dashboard"
        st.rerun()  # 🔥 Força a atualização da interface imediatamente
    else:
        st.error("Usuário ou senha incorretos. Tente novamente.")


def logout():
    """Faz logout e limpa os dados da sessão."""
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.menu = None
    st.rerun()
