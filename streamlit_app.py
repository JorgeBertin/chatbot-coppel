import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Chatbot de Fragancias")

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.step = 0
    st.session_state.respuestas = {}

def add_message(role, text):
    st.session_state.history.append({"role": role, "text": text})

st.sidebar.title(" 📁 Carga tu catálogo")
archivo = st.sidebar.file_uploader("Sube aquí tu catálogo (.xlsx)", type=["xlsx"])
if archivo:
    catalogo = pd.read_excel(archivo)
else:
    st.sidebar.warning("Sube un archivo Excel para empezar")

preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

def ajustar_preguntas(pregs, nombre):
    out = []
    for p in pregs:
        p2 = p.copy()
        p2["texto"] = p2["texto"].replace("tu", f"de {nombre}").replace("¿Qué", "¿Cuál")
        out.append(p2)
    return out

st.title("🤖 Chatbot de Fragancias")
for msg in st.session_state.history:
    st.markdown(f"**{'Bot' if msg['role']=='bot' else 'Tú'}:** {msg['text']}")

if archivo:
    if st.session_state.step == 0:
        add_message("bot", "¿La fragancia es para ti o para regalar?")
        col1, col2 = st.columns(2)
        if col1.button("Para mí"):
            add_message("user", "Para mí")
            st.session_state.nombre = "ti"
            st.session_state.pregs = preguntas_base
            st.session_state.step = 1
        if col2.button("Para regalar"):
            add_message("user", "Para regalar")
            st.session_state.step = 0.5
    elif st.session_state.step == 0.5:
        nombre = st.text_input("¿Cómo se llama la persona?", key="nombre_input")
        if nombre:
            add_message("user", nombre)
            st.session_state.nombre = nombre
            st.session_state.pregs = ajustar_preguntas(preguntas_base, nombre)
            st.session_state.step = 1
    elif 1 <= st.session_state.step <= len(st.session_state.pregs):
        idx = int(st.session_state.step) - 1
        p = st.session_state.pregs[idx]
        add_message("bot", p["texto"])
        sel = st.radio("", p["opciones"], key=f"q{idx}")
        if st.button("Seleccionar", key=f"b{idx}"):
            add_message("user", sel)
            st.session_state.respuestas[p["clave"]] = sel
            st.session_state.step += 1
    else:
        amb = st.session_state.respuestas["ambiente"].lower()
        est = st.session_state.respuestas["estilo"].lower()
        act = st.session_state.respuestas["actividad"].lower()
        inten = st.session_state.respuestas["intensidad"].lower()
        nombre = st.session_state.nombre
        sujeto = "eres" if nombre == "ti" else f"{nombre} es"
        desc = (f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente {amb}, "
                f"con un estilo {est}, y prefiere fragancias de intensidad {inten}. "
                f"Ideal para momentos de {act}.")
        add_message("bot", desc)

        rec = catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        pre_orig = rec["C_precio_original"]
        pre_desc = rec["C_precio_descuento"]
        ahorro = pre_orig - pre_desc
        resultado = (f"Te recomiendo **{prod}**\n\n"
                     f"- Precio original: ${pre_orig:.2f}\n"
                     f"- Precio en línea: ${pre_desc:.2f} (ahorras ${ahorro:.2f})")
        add_message("bot", resultado)

        if st.button("🔄 Empezar de nuevo"):
            st.session_state.history = []
            st.session_state.step = 0
            st.session_state.respuestas = {}
