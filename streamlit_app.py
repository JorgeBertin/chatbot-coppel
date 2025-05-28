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
    st.button("🔄 Reiniciar encuesta", on_click=lambda: st.session_state.clear())

# --- Preguntas base ---
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define


