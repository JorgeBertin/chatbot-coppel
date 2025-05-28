import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# --- Preguntas base ---
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

# Función para ajustar preguntas si es regalo
def ajustar_para_regalo(pregs, nombre):
    preg_regalo = []
    for p in pregs:
        p_nueva = p.copy()
        p_nueva["texto"] = p_nueva["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}").replace("¿Qué", "¿Cuál")
        preg_regalo.append(p_nueva)
    return preg_regalo

# Función para agregar mensaje al historial
def add_message(autor, texto):
    st.session_state.history.append((autor, texto))

# Inicialización estado
if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "pregs" not in st.session_state:
    st.session_state.pregs = []
if "nombre" not in st.session_state:
    st.session_state.nombre = "ti"
if "catalogo" not in st.session_state:
    st.session_state.catalogo = None

st.title("💬 Chatbot Coppel")

# Sidebar para cargar catálogo
uploaded = st.sidebar.file_uploader("Sube el catálogo (Excel .xlsx)", type=["xlsx"])
if uploaded is not None:
    st.session_state.catalogo = pd.read_excel(uploaded)

# Mostrar historial chat
for autor, texto in st.session_state.history:
    with st.chat_message(autor):
        st.markdown(texto)

# Paso 0: Pregunta inicial (para ti o regalar)
if st.session_state.step == 0:
    st.markdown("**Bot:** ¿La fragancia es para ti o para regalar?")
    opcion = st.radio("Selecciona:", ["Para mí", "Para regalar"], key="opt0")
    if st.button("Enviar", key="btn0"):
        add_message("user",_







