import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# --- Inicializar session_state ---
defaults = {
    "step": 0,
    "nombre": "",
    "pregs": [],
    "respuestas": {},
    "history": [],
    "catalogo": None,
    # flags para controlar renderizado
    "shown_initial": False,
    "shown_name": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Funciones auxiliares ---
def add_message(author, text):
    st.session_state.history.append((author, text))

def load_catalog(file):
    return pd.read_excel(file)

# --- Sidebar: uploader + reiniciar ---
with st.sidebar:
    st.title("📦 Catálogo")
    upload = st.file_uploader("Sube tu catálogo (.xlsx)", type=["xlsx"])
    if upload:
        st.session_state.catalogo = load_catalog(upload)
        st.success("Catálogo cargado.")
    if st.button("🔄 Reiniciar todo"):
        for k in defaults: st.session_state[k] = defaults[k]

# --- Preguntas base ---
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque","Playa","Ciudad"]},
    {"clave": "estilo",   "texto": "¿Qué estilo te define mejor?",      "opciones": ["Elegante","Deportivo","Romántico"]},
    {"clave": "actividad","texto": "¿Qué actividad disfrutas más?",   "opciones": ["Salir de noche","Viajar","Leer un libro"]},
    {"clave": "clima",    "texto": "¿Qué clima prefieres?",            "opciones": ["Cálido","Frío","Templado"]},
    {"clave": "intensidad","texto":"¿Qué intensidad de aroma prefieres?","opciones":["Suave","Moderado","Intenso"]},
    {"clave": "momento",  "texto": "¿Para qué momento la usarías?",    "opciones":["Día","Noche","Ambos"]},
]

def ajustar_para_regalo(lst, nombre):
    out=[]
    for p in lst:
        p2=p.copy()
        p2["texto"] = p2["texto"].replace("tu", f"de {nombre}").replace("¿Qué","¿Cuál")
        out.append(p2)
    return out

# --- Mostrar todo el historial tipo chat ---
st.title("💬 Chatbot Coppel")
for author, msg in st.session_state.history:
    with st.chat_message(author):
        st.markdown(msg)

# --- STEP 0: Pregunta inicial ---
if st.session_state.step == 0:
    # 0a) mostrar pregunta
    if not st.session_state.shown_initial:
        add_message("bot", "¿La fragancia es para ti o para regalar?")
        st.session_state.shown_initial = True
        st.experimental_rerun()

    # 0b) recoger respuesta
    opcion = st.radio("Selecciona:", ["Para mí", "Para regalar"], key="opt0")
    if st.button("Enviar", key="btn0"):
        add_message("user", opcion)
        if opcion == "Para mí":
            st.session_state.nombre = "ti"
            st.session_state.pregs = preguntas_base
            st.session_state.step = 1
        else:
            st.session_state.step = -1
        st.experimental_rerun()

# --- STEP -1: Si es regalo, pedimos nombre ---
elif st.session_state.step == -1:
    if not st.session_state.shown_name:
        add_message("bot", "¿Cómo se llama la persona a la que vas a regalar la fragancia?")
        st.session_state.shown_name = True
        st.experimental_rerun()

    nombre = st.text_input("Nombre del destinatario",_



