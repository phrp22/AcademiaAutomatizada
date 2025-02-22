import streamlit as st

# Lista de escalas disponíveis
scales = ["Ansiedade", "Depressão", "Estresse"]

def show_professional_dashboard():
    """Tela do profissional com opções de cadastro e envio de escalas."""
    st.subheader("Área exclusiva para Profissionais")
    st.write("Cadastre um paciente para enviar uma escala.")

    # Formulário para cadastrar um paciente
    patient_username = st.text_input("Nome de usuário do paciente")

    if st.button("Adicionar Paciente"):
        if patient_username:
            if "patients" not in st.session_state:
                st.session_state.patients = {}
            if patient_username not in st.session_state.patients:
                st.session_state.patients[patient_username] = {}  # Inicializa corretamente como dicionário
            st.success(f"Paciente {patient_username} cadastrado com sucesso!")
        else:
            st.error("Digite um nome de usuário válido.")

    st.write("---")  # Separador

    # Selecionar um paciente e uma escala para enviar
    if st.session_state.patients:
        selected_patient = st.selectbox("Selecione um paciente", list(st.session_state.patients.keys()))
        selected_scales = st.multiselect("Selecione as escalas para enviar", scales)

        if st.button("Enviar Escalas"):
            for scale in selected_scales:
                st.session_state.patients[selected_patient][scale] = "pendente"
            st.success(f"Escalas enviadas para {selected_patient}!")