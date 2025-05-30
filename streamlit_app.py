import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbot Coppel", layout="centered")

# 1. Catálogo
catalogo = st.sidebar.file_uploader("Sube el catálogo (Excel .xlsx)", type=["xlsx"])
if catalogo:
    df_catalogo = pd.read_excel(catalogo)
else:
    df_catalogo = None

# 2. Preguntas base
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

def ajustar_para_regalo(pregs, nombre):
    # Personaliza las preguntas para regalo
    out = []
    for p in pregs:
        t = p["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}")
        out.append({"clave": p["clave"], "texto": t, "opciones": p["opciones"]})
    return out

# 3. Estado inicial
if "history" not in st.session_state:
    st.session_state.history = []
if "paso" not in st.session_state:
    st.session_state.paso = 0  # 0=quién, -1=nombre regalo, >=1=resto
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "nombre" not in st.session_state:
    st.session_state.nombre = "ti"
if "pregs" not in st.session_state:
    st.session_state.pregs = []

st.title("💬 Chatbot Coppel")

# 4. Mostrar historial tipo chat
for autor, texto in st.session_state.history:
    with st.chat_message(autor):
        st.markdown(texto)

# 5. Flujo del chatbot
### PASO 0: ¿Para ti o para regalar?
if st.session_state.paso == 0:
    with st.chat_message("bot"):
        st.markdown("¿La fragancia es para ti o para regalar?")

    form = st.form("form_tipo")
    opcion = form.radio("Selecciona:", ["Para mí", "Para regalar"], key="radio_tipo")
    enviar = form.form_submit_button("Enviar")
    if enviar:
        st.session_state.respuestas["tipo"] = opcion
        st.session_state.history.append(("user", opcion))
        if opcion == "Para mí":
            st.session_state.pregs = preguntas_base
            st.session_state.paso = 1
            st.session_state.nombre = "ti"
        else:
            st.session_state.paso = -1

### PASO -1: Preguntar nombre para regalar
elif st.session_state.paso == -1:
    with st.chat_message("bot"):
        st.markdown("¿Cómo se llama la persona a la que vas a regalar la fragancia?")
    form = st.form("form_nombre")
    nombre = form.text_input("Nombre del destinatario", key="nombre_regalo")
    enviar = form.form_submit_button("Enviar")
    if enviar and nombre.strip():
        st.session_state.nombre = nombre.strip()
        st.session_state.history.append(("user", nombre.strip()))
        st.session_state.pregs = ajustar_para_regalo(preguntas_base, st.session_state.nombre)
        st.session_state.paso = 1

### PASO >=1: Preguntas personalizadas
elif 1 <= st.session_state.paso <= len(st.session_state.pregs):
    idx = st.session_state.paso - 1
    pregunta = st.session_state.pregs[idx]
    with st.chat_message("bot"):
        st.markdown(pregunta["texto"])
    form = st.form(f"form_{pregunta['clave']}")
    opcion = form.radio("Elige una opción:", pregunta["opciones"], key=f"radio_{pregunta['clave']}")
    enviar = form.form_submit_button("Enviar")
    if enviar and opcion:
        st.session_state.respuestas[pregunta["clave"]] = opcion
        st.session_state.history.append(("user", opcion))
        st.session_state.paso += 1

### FINAL: Mostrar resultado y recomendación
elif st.session_state.paso > len(st.session_state.pregs):
    nombre = st.session_state.nombre
    r = st.session_state.respuestas
    sujeto = "eres" if nombre == "ti" else f"{nombre} es"
    descripcion = (
        f"¡Gracias! Según tus respuestas, {sujeto} alguien que disfruta del ambiente **{r['ambiente'].lower()}**, "
        f"con un estilo **{r['estilo'].lower()}**, y prefiere fragancias de intensidad **{r['intensidad'].lower()}**. "
        f"Ideal para momentos de **{r['actividad'].lower()}**."
    )
    if not st.session_state.history or st.session_state.history[-1][1] != descripcion:
        st.session_state.history.append(("bot", descripcion))

    # Recomendación de producto
    if df_catalogo is not None:
        rec = df_catalogo.sample(1).iloc[0]
        prod = rec["C_producto"]
        po = rec["C_precio_original"]
        pd = rec["C_precio_descuento"]
        ahorro = po - pd
        texto_rec = (
            f"Te recomendamos **{prod}**\n\n"
            f"- Precio original: ${po:.2f}\n"
            f"- Precio con descuento: ${pd:.2f} (ahorras ${ahorro:.2f})"
        )
        if not st.session_state.history or st.session_state.history[-1][1] != texto_rec:
            st.session_state.history.append(("bot", texto_rec))
    else:
        msg = "Por favor sube el catálogo en la barra lateral para recomendarte."
        if not st.session_state.history or st.session_state.history[-1][1] != msg:
            st.session_state.history.append(("bot", msg))
