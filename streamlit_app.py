import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# --- CSS para compactar los mensajes de chat ---
st.markdown("""
    <style>
    div[data-testid="stChatMessage"] {
        padding: 8px 16px !important;
        margin-bottom: 2px !important;
        min-height: 8px !important;
    }
    .stChatMessageContent {
        padding: 3px 0 !important;
    }
    .stChatMessageIcon {
        margin-right: 6px !important;
        margin-left: 0 !important;
    }
    .block-container {
        padding-top: 35px !important;
    }
    </style>
""", unsafe_allow_html=True)
# --- BANNER AMARILLO CON LOGO Y TÍTULO ---
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("coppel_logo4.png")
    with col2:
        st.markdown(
            "<span style='font-family: Montserrat, Arial, sans-serif; font-size: 1.7rem; color: #174ea6; font-weight: 700; vertical-align: middle;'>Chatbot Coppel</span>",
            unsafe_allow_html=True
        )

# --- PREGUNTAS BASE ---
preguntas_base = [
    {"clave": "sexo", "texto": "¿Cuál es tu sexo?", "opciones": ["Masculino", "Femenino"]},
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

def add_message(autor, texto):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append((autor, texto))

# Inicialización de session_state
if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = 1  # ← Arranca en 1, ya no hay paso 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "pregs" not in st.session_state:
    st.session_state.pregs = preguntas_base
if "nombre" not in st.session_state:
    st.session_state.nombre = "ti"
if "catalogo_hombres" not in st.session_state:
    st.session_state.catalogo_hombres = None
if "catalogo_mujeres" not in st.session_state:
    st.session_state.catalogo_mujeres = None

# Subir catálogos por sexo
uploaded_hombres = st.sidebar.file_uploader("Sube el catálogo de HOMBRES (Excel .xlsx)", type=["xlsx"], key="hombres")
uploaded_mujeres = st.sidebar.file_uploader("Sube el catálogo de MUJERES (Excel .xlsx)", type=["xlsx"], key="mujeres")

if uploaded_hombres:
    st.session_state.catalogo_hombres = pd.read_excel(uploaded_hombres)
if uploaded_mujeres:
    st.session_state.catalogo_mujeres = pd.read_excel(uploaded_mujeres)

# Mostrar historial chat SIN avatar, solo "Bot:" y "Tú:"
for autor, texto in st.session_state.history:
    if autor == "bot":
        with st.chat_message("assistant"):
            st.markdown(f"**Bot:** {texto}")
    elif autor == "user":
        with st.chat_message("user"):
            st.markdown(f"**Tú:** {texto}")

# Flujo de preguntas y respuestas
if 1 <= st.session_state.step <= len(st.session_state.pregs):
    idx = st.session_state.step - 1
    preg = st.session_state.pregs[idx]
    with st.chat_message("assistant"):
        st.markdown(f"**Bot:** {preg['texto']}")
    opcion = st.radio("", preg["opciones"], key=f"opt{idx}")
    if st.button("Enviar", key=f"btn{idx}"):
        add_message("bot", preg["texto"])
        add_message("user", opcion)
        st.session_state.respuestas[preg["clave"]] = opcion
        st.session_state.step += 1

else:
    nombre = st.session_state.nombre
    r = st.session_state.respuestas
    sujeto = "eres" if nombre == "ti" else f"{nombre} es"
    descripcion = (f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente **{r['ambiente'].lower()}**, "
                   f"con un estilo **{r['estilo'].lower()}**, y prefiere fragancias de intensidad **{r['intensidad'].lower()}**. "
                   f"Ideal para momentos de **{r['actividad'].lower()}**.")
    add_message("bot", descripcion)

    sexo_usuario = st.session_state.respuestas.get("sexo", None)
    if sexo_usuario == "Masculino":
        catalogo = st.session_state.catalogo_hombres
        tipo = "hombres"
    elif sexo_usuario == "Femenino":
        catalogo = st.session_state.catalogo_mujeres
        tipo = "mujeres"
    else:
        catalogo = None
        tipo = ""

    if catalogo is not None and len(catalogo) > 0:
        rec = catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        po = rec["C_precio_original"]
        pd = rec["C_precio_descuento"]
        ahorro = po - pd
        texto_rec = (f"Te recomendamos **{prod}**\n\n"
                     f"- Precio original: ${po:.2f}\n"
                     f"- Precio con descuento: ${pd:.2f} (ahorras ${ahorro:.2f})")
        add_message("bot", texto_rec)
    else:
        add_message("bot", f"Por favor sube el catálogo de {tipo} en la barra lateral para recomendarte.")

    # Mostrar últimos mensajes (evitar repetir todo el historial)
    for autor, texto in st.session_state.history[-4:]:
        if autor == "bot":
            with st.chat_message("assistant"):
                st.markdown(f"**Bot:** {texto}")
        elif autor == "user":
            with st.chat_message("user"):
                st.markdown(f"**Tú:** {texto}")

