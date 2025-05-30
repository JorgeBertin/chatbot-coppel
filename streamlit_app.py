import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

def ajustar_para_regalo(pregs, nombre):
    preg_regalo = []
    for p in pregs:
        p_nueva = p.copy()
        p_nueva["texto"] = p_nueva["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}").replace("¿Qué", "¿Cuál")
        preg_regalo.append(p_nueva)
    return preg_regalo

def add_message(autor, texto):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append((autor, texto))

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

uploaded = st.sidebar.file_uploader("Sube el catálogo (Excel .xlsx)", type=["xlsx"])
if uploaded:
    st.session_state.catalogo = pd.read_excel(uploaded)

# Mostrar historial de mensajes
for autor, texto in st.session_state.history:
    with st.chat_message(autor):
        st.markdown(texto)

# PREGUNTA 0: ¿Para ti o para regalar?
if st.session_state.step == 0:
    opcion = st.radio("**Bot:** ¿La fragancia es para ti o para regalar?", ["Para mí", "Para regalar"], key="opt0")
    if st.button("Enviar", key="btn0") and opcion:
        add_message("user", opcion)
        st.session_state.respuestas["tipo"] = opcion
        if opcion == "Para mí":
            st.session_state.nombre = "ti"
            st.session_state.pregs = preguntas_base
            st.session_state.step = 1
        else:
            st.session_state.step = -1

# PREGUNTA DE NOMBRE PARA REGALO
elif st.session_state.step == -1:
    nombre = st.text_input("**Bot:** ¿Cómo se llama la persona a la que vas a regalar la fragancia?", key="nombre")
    if st.button("Enviar", key="btn_name") and nombre.strip():
        st.session_state.nombre = nombre.strip()
        add_message("user", st.session_state.nombre)
        st.session_state.pregs = ajustar_para_regalo(preguntas_base, st.session_state.nombre)
        st.session_state.step = 1

# CICLO DE PREGUNTAS PERSONALIZADAS
elif 1 <= st.session_state.step <= len(st.session_state.pregs):
    idx = st.session_state.step - 1
    preg = st.session_state.pregs[idx]
    opcion = st.radio(f"**Bot:** {preg['texto']}", preg["opciones"], key=f"opt{idx}")

    # Aquí viene el truco: validamos que sí haya respuesta seleccionada antes de avanzar
    if st.button("Enviar", key=f"btn{idx}") and opcion:
        st.session_state.respuestas[preg["clave"]] = opcion
        add_message("user", opcion)
        st.session_state.step += 1

# MENSAJE FINAL Y RECOMENDACIÓN
else:
    nombre = st.session_state.nombre
    r = st.session_state.respuestas
    sujeto = "eres" if nombre == "ti" else f"{nombre} es"
    descripcion = (f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente **{r['ambiente'].lower()}**, "
                   f"con un estilo **{r['estilo'].lower()}**, y prefiere fragancias de intensidad **{r['intensidad'].lower()}**. "
                   f"Ideal para momentos de **{r['actividad'].lower()}**.")
    if not st.session_state.history or st.session_state.history[-1][1] != descripcion:
        add_message("bot", descripcion)

    if st.session_state.catalogo is not None:
        rec = st.session_state.catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        po = rec["C_precio_original"]
        pd = rec["C_precio_descuento"]
        ahorro = po - pd
        texto_rec = (f"Te recomendamos **{prod}**\n\n"
                     f"- Precio original: ${po:.2f}\n"
                     f"- Precio con descuento: ${pd:.2f} (ahorras ${ahorro:.2f})")
        if not st.session_state.history or st.session_state.history[-1][1] != texto_rec:
            add_message("bot", texto_rec)
    else:
        mensaje_catalogo = "Por favor sube el catálogo en la barra lateral para recomendarte."
        if not st.session_state.history or st.session_state.history[-1][1] != mensaje_catalogo:
            add_message("bot", mensaje_catalogo)

    for autor, texto in st.session_state.history[-6:]:
        with st.chat_message(autor):
            st.markdown(texto)
