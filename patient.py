import streamlit as st
from database import save_scale_responses

# Lista de escalas (deve ser a mesma do professional.py)
scales = {
    "Ansiedade": [
        "Você se sente ansioso(a) frequentemente?",
        "Você tem dificuldades para dormir?",
        "Você se sente cansado(a) durante o dia?",
        "Você tem dificuldade para se concentrar?",
        "Você se sente sobrecarregado(a) com as tarefas diárias?"
    ],
    "Depressão": [
        "Você se sente triste ou desmotivado(a) frequentemente?",
        "Você sente mudanças no seu apetite?",
        "Você tem dificuldades para interagir socialmente?",
        "Você sente dores físicas sem explicação?",
        "Você se sente satisfeito(a) com sua vida atualmente?"
    ],
    "Estresse": [
        "Você se sente constantemente sob pressão?",
        "Você tem dificuldades para relaxar?",
        "Você se sente irritado(a) facilmente?",
        "Você tem tensão muscular frequente?",
        "Você tem dificuldades para controlar preocupações?"
    ]
}

def show_patient_dashboard():
    """Tela para o paciente responder a escala."""
    patient_username = st.session_state.user

    if patient_username in st.session_state.patients:
        pending_scales = {scale: status for scale, status in st.session_state.patients[patient_username].items() if status == "pendente"}

        if pending_scales:
            selected_scale = st.selectbox("Você tem escalas pendentes. Escolha uma para responder:", list(pending_scales.keys()))

            st.subheader(f"Escala: {selected_scale}")

            responses = []
            all_answered = True  # Variável para verificar se todas as perguntas foram respondidas

            for question in scales[selected_scale]:
                response = st.radio(
                    question,
                    ["Selecione uma opção", "Nunca", "Às vezes", "Frequentemente", "Sempre"],
                    index=0,  # Define a opção padrão como "Selecione uma opção"
                    key=f"{selected_scale}_{question}"
                )

                # Se o usuário não selecionou nada além da opção padrão, impede o envio
                if response == "Selecione uma opção":
                    all_answered = False

                responses.append(response if response != "Selecione uma opção" else None)

            # Criamos um único botão de envio
            if st.button("Enviar Respostas", key="submit_button"):
                if all_answered:
                    sucesso = save_scale_responses(patient_username, selected_scale, responses)

                    if sucesso:
                        st.session_state.patients[patient_username][selected_scale] = "respondido"
                        st.success(f"Respostas enviadas para a escala '{selected_scale}' e salvas no Supabase!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar respostas. Tente novamente.")
                else:
                    st.error("⚠️ Você deve responder todas as perguntas antes de enviar!")

        else:
            st.info("Nenhuma escala pendente para responder.")
    else:
        st.info("Você não tem escalas atribuídas.")
