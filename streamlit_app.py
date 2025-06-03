import streamlit as st
import pandas as pd
import random
import datetime
import os

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

# --- BANNER CON LOGO Y TÍTULO ---
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
    {
        "clave": "inicio",
        "texto": "Hola, soy el nuevo chatbot de fragancias de Coppel. ¿Estás listo para empezar con el test?",
        "opciones": ["Sí", "No"]
    },
    {
        "clave": "sexo",
        "texto": "¿Cuál es tu sexo?  \n*Si es para regalo, trata de contestar como esa persona.*",
        "opciones": ["Masculino", "Femenino"]
    },
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

# --- RESPALDO HOMBRES ---
respaldo_hombres = [
    {
        "C_producto": "Perfume Versace Dreamer Eau De Toilette 100 Ml Para Hombre - Venta Internacional.",
        "C_precio_original": 1489,
        "C_precio_descuento": 1266
    },
    {
        "C_producto": "Venta Internacional - Perfume Versace Pour Homme para Hombre Edt 100 Ml",
        "C_precio_original": 2127,
        "C_precio_descuento": 1872
    },
    {
        "C_producto": "Venta Internacional - Perfume Carolina Herrera 212 Vip Black Para Hombre Edt 100ml",
        "C_precio_original": 2791,
        "C_precio_descuento": 2699
    },
    {
        "C_producto": "Perfume Carolina Herrera 212 de 200 ml Edt Spray para Hombre",
        "C_precio_original": 3499,
        "C_precio_descuento": 2099
    },
    {
        "C_producto": "Venta Internacional - Perfume Hugo Boss Boss Number One Edt 100 Ml para Hombre",
        "C_precio_original": 1379,
        "C_precio_descuento": 1214
    },
    {
        "C_producto": "Perfume Salvatore Ferragamo Uomo Urban Feel Edt 100 Ml para Hombre - Venta Internacional",
        "C_precio_original": 1514,
        "C_precio_descuento": 1333
    },
]

# --- RESPALDO MUJERES ---
respaldo_mujeres = [
    {
        "C_producto": "Perfume Carolina Herrera 212 Vip Rosé 80 ml Edp Original para Dama",
        "C_precio_original": 1848,
        "C_precio_descuento": 2981
    },
    {
        "C_producto": "Perfume Carolina Herrera Good Girl Eau de Parfum 150 ml para Mujer",
        "C_precio_original": 2563,
        "C_precio_descuento": 3770
    },
    {
        "C_producto": "Perfume Carolina Herrera Good Girl Eau de Parfum 100 ml para Mujer",
        "C_precio_original": 4140,
        "C_precio_descuento": 4599
    },
    {
        "C_producto": "Perfume Dior Hypnotic Poison Eau De Toilette 30 Ml Para Mujer - Venta Internacional.",
        "C_precio_original": 1877,
        "C_precio_descuento": 2606
    },
    {
        "C_producto": "Perfume Dior Addict de Christian Dior Eau de Toilette de 100 ml para Mujer",
        "C_precio_original": 2121,
        "C_precio_descuento": 4079
    },
    {
        "C_producto": "Perfume The Merchant Of Venice Damascus Desert Eau De Parfum 100 Ml - Venta Internacional",
        "C_precio_original": 2301,
        "C_precio_descuento": 2614
    },
    {
        "C_producto": "Perfume Chanel Coco Mademoiselle Edp para Mujer-Venta Internacional",
        "C_precio_original": 914,
        "C_precio_descuento": 900
    },
    {
        "C_producto": "Perfume Yves Saint Laurent Libre Eau De Toilette 90 ml para Mujer",
        "C_precio_original": 2389,
        "C_precio_descuento": 3109
    },
    {
        "C_producto": "Perfume Yves Saint Laurent Paris Eau De Toilette 125 Ml Para Mujer - Venta Internacional",
        "C_precio_original": 3365,
        "C_precio_descuento": 3823
    },
]

def add_message(autor, texto):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append((autor, texto))

# Inicialización de session_state
if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = 1  # Ahora inicia con la primera pregunta
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

# AUTOSCROLL marcador después del historial
st.markdown('<div id="chat_end"></div>', unsafe_allow_html=True)

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

        # Si responde "No" en la bienvenida, termina el flujo con un mensaje de despedida
        if preg["clave"] == "inicio" and opcion == "No":
            add_message("bot", "¡No hay problema! Cuando quieras, vuelve a iniciar el test. 😊")
            st.session_state.step = len(st.session_state.pregs) + 1  # Salta al final
        else:
            st.session_state.step += 1

else:
    nombre = st.session_state.nombre
    r = st.session_state.respuestas
    if r.get("inicio") == "No":
        # Ya se mostró el mensaje de despedida, no hacer más.
        pass
    else:
        sujeto = "eres" if nombre == "ti" else f"{nombre} es"
        descripcion = (f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente **{r.get('ambiente','').lower()}**, "
                    f"con un estilo **{r.get('estilo','').lower()}**, y prefiere fragancias de intensidad **{r.get('intensidad','').lower()}**. "
                    f"Ideal para momentos de **{r.get('actividad','').lower()}**.")
        add_message("bot", descripcion)

        # --- CORRECCIÓN DEL RESPALDO ---
        sexo_usuario = st.session_state.respuestas.get("sexo", "").strip().lower()
        if sexo_usuario == "masculino":
            catalogo = st.session_state.catalogo_hombres
            tipo = "hombres"
            respaldo = respaldo_hombres
        elif sexo_usuario == "femenino":
            catalogo = st.session_state.catalogo_mujeres
            tipo = "mujeres"
            respaldo = respaldo_mujeres
        else:
            catalogo = None
            respaldo = []
            tipo = ""

        if catalogo is not None and len(catalogo) > 0:
            muestras = catalogo.sample(min(3, len(catalogo)))
            recomendaciones = []
            for _, rec in muestras.iterrows():
                prod = rec["C_producto"]
                po = rec["C_precio_original"]
                pd = rec["C_precio_descuento"]
                ahorro = po - pd
                recomendaciones.append(
                    f"- **{prod}**\n"
                    f"    - Precio original: ${po:.2f}\n"
                    f"    - Precio con descuento: ${pd:.2f}\n"
                    f"    - **Ahorras: ${ahorro:.2f}**"
                )
            texto_rec = "Te recomendamos las siguientes fragancias:\n\n" + "\n\n".join(recomendaciones)
            add_message("bot", texto_rec)
        elif respaldo and len(respaldo) > 0:
            muestras = random.sample(respaldo, min(3, len(respaldo)))
            recomendaciones = []
            for rec in muestras:
                prod = rec["C_producto"]
                po = rec["C_precio_original"]
                pd = rec["C_precio_descuento"]
                ahorro = po - pd
                recomendaciones.append(
                    f"- **{prod}**\n"
                    f"    - Precio original: ${po:.2f}\n"
                    f"    - Precio con descuento: ${pd:.2f}\n"
                    f"    - **Ahorras: ${ahorro:.2f}**"
                )
            texto_rec = (
                "Te recomendamos las siguientes fragancias (usando catálogo de respaldo de Coppel):\n\n" +
                "\n\n".join(recomendaciones)
            )
            add_message("bot", texto_rec)
        else:
            add_message("bot", f"Por favor sube el catálogo de {tipo} en la barra lateral para recomendarte.")

        # Mostrar últimos mensajes del historial
        for autor, texto in st.session_state.history[-2:]:
            if autor == "bot":
                with st.chat_message("assistant"):
                    st.markdown(f"**Bot:** {texto}")
            elif autor == "user":
                with st.chat_message("user"):
                    st.markdown(f"**Tú:** {texto}")

        st.markdown('<div id="chat_end"></div>', unsafe_allow_html=True)
        st.markdown("""
            <script>
            setTimeout(function() {
                var chatEnd = document.getElementById('chat_end');
                if (chatEnd) { chatEnd.scrollIntoView({ behavior: 'smooth' }); }
            }, 300);
            </script>
        """, unsafe_allow_html=True)


