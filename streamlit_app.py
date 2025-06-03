import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# --- CSS para compactar los mensajes de chat ---
st.markdown("""
    <style>
    /* Solo compacta las burbujas que están debajo del header */
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
    /* Opcional: espacio arriba y abajo de la cabecera */
    .block-container {
        padding-top: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)
# --- BANNER AMARILLO CON LOGO Y TÍTULO ---
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("coppel_logo4.png")  # Ajusta el width si lo quieres más pequeño
    with col2:
        st.markdown(
            "<span style='font-family: Montserrat, Arial, sans-serif; font-size: 1.7rem; color: #174ea6; font-weight: 700; vertical-align: middle;'>Chatbot Coppel</span>",
            unsafe_allow_html=True
        )
# --- RESTO DE LA APP ---
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

# Inicialización de session_state
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

# Subir catálogo
uploaded = st.sidebar.file_uploader("Sube el catálogo (Excel .xlsx)", type=["xlsx"])
if uploaded:
    st.session_state.catalogo = pd.read_excel(uploaded)

# Mostrar historial chat
for autor, texto in st.session_state.history:
    with st.chat_message(autor):
        st.markdown(texto)

if st.session_state.step == 0:
    pregunta_inicial = "¿La fragancia es para ti o para regalar?"
    st.markdown(f"**Bot:** {pregunta_inicial}")
    opcion = st.radio("Selecciona:", ["Para mí", "Para regalar"], key="opt0")
    if st.button("Enviar", key="btn0"):
        add_message("bot", pregunta_inicial)
        add_message("user", opcion)
        if opcion == "Para mí":
            st.session_state.nombre = "ti"
            st.session_state.pregs = preguntas_base
            st.session_state.step = 1
        else:
            st.session_state.step = -1

elif st.session_state.step == -1:
    pregunta_nombre = "¿Cómo se llama la persona a la que vas a regalar la fragancia?"
    st.markdown(f"**Bot:** {pregunta_nombre}")
    nombre = st.text_input("Nombre del destinatario", key="nombre")
    if st.button("Enviar", key="btn_name") and nombre.strip():
        add_message("bot", pregunta_nombre)
        add_message("user", nombre.strip())
        st.session_state.nombre = nombre.strip()
        st.session_state.pregs = ajustar_para_regalo(preguntas_base, nombre.strip())
        st.session_state.step = 1

elif 1 <= st.session_state.step <= len(st.session_state.pregs):
    idx = st.session_state.step - 1
    preg = st.session_state.pregs[idx]
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

    if st.session_state.catalogo is not None:
        rec = st.session_state.catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        po = rec["C_precio_original"]
        pd = rec["C_precio_descuento"]
        ahorro = po - pd
        texto_rec = (f"Te recomendamos **{prod}**\n\n"
                     f"- Precio original: ${po:.2f}\n"
                     f"- Precio con descuento: ${pd:.2f} (ahorras ${ahorro:.2f})")
        add_message("bot", texto_rec)
    else:
        add_message("bot", "Por favor sube el catálogo en la barra lateral para recomendarte.")

    # Mostrar últimos mensajes (evitar repetir todo el historial)
    for autor, texto in st.session_state.history[-4:]:
        with st.chat_message(autor):
            st.markdown(texto)



