import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# --- Inicializar estados ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "catalogo" not in st.session_state:
    st.session_state.catalogo = None
if "pregs" not in st.session_state:
    st.session_state.pregs = []

# --- Cargar Excel desde la barra lateral ---
with st.sidebar:
    st.title("📦 Catálogo")
    archivo = st.file_uploader("Sube el archivo Excel del catálogo", type=["xlsx"])
    if archivo:
        st.session_state.catalogo = pd.read_excel(archivo)
        st.success("Catálogo cargado correctamente.")

# --- Preguntas base ---
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

def ajustar_preguntas_para_regalo(preguntas, nombre):
    preguntas_regalo = []
    for p in preguntas:
        p_nueva = p.copy()
        p_nueva["texto"] = p_nueva["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}").replace("¿Qué", "¿Cuál")
        preguntas_regalo.append(p_nueva)
    return preguntas_regalo

def add_message(autor, mensaje):
    st.session_state.history.append((autor, mensaje))

# --- Mostrar conversación tipo chat ---
st.title("💬 Chatbot Coppel")

for autor, mensaje in st.session_state.history:
    with st.chat_message(autor):
        st.markdown(mensaje)

# --- Paso 0: ¿Es para ti o para regalo? ---
if st.session_state.step == 0:
    with st.chat_message("bot"):
        st.markdown("¿La fragancia es para ti o para regalar?")
    opcion = st.radio("Selecciona una opción:", ["Para mí", "Para rega]()

