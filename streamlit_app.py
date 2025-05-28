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
    if not st.session_state.shown_initial:
        add_message("bot", "¿La fragancia es para ti o para regalar?")
        st.session_state.shown_initial = True
        st.experimental_rerun()

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

    nombre = st.text_input("Nombre del destinatario")
    if st.button("Enviar", key="btn_name") and nombre.strip():
        add_message("user", nombre.strip())
        st.session_state.nombre = nombre.strip()
        st.session_state.pregs = ajustar_para_regalo(preguntas_base, nombre.strip())
        st.session_state.step = 1
        st.experimental_rerun()

# --- STEPS 1..N: Preguntas de la encuesta ---
elif 1 <= st.session_state.step <= len(st.session_state.pregs):
    idx = st.session_state.step - 1
    preg = st.session_state.pregs[idx]
    key_shown = f"shown_{idx}"
    key_ans   = f"ans_{idx}"

    if not st.session_state.get(key_shown, False):
        add_message("bot", preg["texto"])
        st.session_state[key_shown] = True
        st.experimental_rerun()

    if not st.session_state.get(key_ans, False):
        choice = st.radio("", preg["opciones"], key=f"opt{idx}")
        if st.button("Enviar", key=f"btn{idx}"):
            add_message("user", choice)
            st.session_state.respuestas[preg["clave"]] = choice
            st.session_state[key_ans] = True
            st.session_state.step += 1
            st.experimental_rerun()

# --- STEP final: mostrar recomendación ---
else:
    nombre = st.session_state.nombre
    r = st.session_state.respuestas
    sujeto = "eres" if nombre=="ti" else f"{nombre} es"
    desc = (f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente **{r['ambiente'].lower()}**, "
            f"con un estilo **{r['estilo'].lower()}**, y prefiere fragancias de intensidad **{r['intensidad'].lower()}**. "
            f"Ideal para momentos de **{r['actividad'].lower()}**.")
    add_message("bot", desc)

    if st.session_state.catalogo is not None:
        rec = st.session_state.catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        po = rec["C_precio_original"]
        pd = rec["C_precio_descuento"]
        ahorro = po - pd
        tex = (f"Te recomendamos **{prod}**\n\n"
               f"- Precio original: ${po:.2f}\n"
               f"- Precio con descuento: ${pd:.2f} (ahorras ${ahorro:.2f})")
        add_message("bot", tex)
    else:
        add_message("bot", "Por favor sube el catálogo en la barra lateral para recomendarte.")

    st.session_state.step += 1




