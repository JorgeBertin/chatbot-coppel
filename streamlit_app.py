import streamlit as st

# Función para agregar mensajes a la conversación en sesión
def add_message(sender, text):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({"sender": sender, "text": text})

# Inicializar variables de sesión
if "step" not in st.session_state:
    st.session_state.step = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

should_rerun = False  # Flag para controlar rerun

# Paso 0: pregunta inicial
if st.session_state.step == 0:
    opcion = st.radio("¿La fragancia es para ti o para regalar?", ["Para mí", "Para regalar"])
    if st.button("Enviar", key="btn_0"):
        add_message("user", opcion)
        st.session_state.para_regalo = opcion
        if opcion == "Para regalar":
            st.session_state.step = 0.5
        else:
            st.session_state.step = 1
            st.session_state.sexo = None
        should_rerun = True

# Paso 0.5: si es para regalar, pedir nombre
elif st.session_state.step == 0.5:
    nombre = st.text_input("Nombre del destinatario")
    if st.button("Enviar", key="btn_0_5"):
        add_message("user", nombre)
        st.session_state.nombre = nombre
        st.session_state.step = 1
        st.session_state.sexo = None
        should_rerun = True

# Paso 1: pregunta de sexo
elif st.session_state.step == 1:
    sexo = st.radio("Sexo (para recomendar fragancias adecuadas):", ["M", "F"])
    if st.button("Enviar", key="btn_1"):
        add_message("user", sexo)
        st.session_state.sexo = sexo
        st.session_state.step = 2
        should_rerun = True

# Aquí continuar con los siguientes pasos de la encuesta...

# Finalmente, si flag para rerun está activo, hacemos rerun
if should_rerun:
    st.experimental_rerun()

# Mostrar conversación
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f"**Tú:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")


