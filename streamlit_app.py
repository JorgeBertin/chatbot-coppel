import streamlit as st
import pandas as pd
import random

# Carga el catálogo (asegúrate que esté en el mismo directorio que el script)
catalogo = pd.read_excel("catalogo coppel.xlsx")

# Preguntas base
preguntas_base = [
    {"clave": "ambiente", "texto": "¿Cuál es tu ambiente favorito?", "opciones": ["Bosque", "Playa", "Ciudad"]},
    {"clave": "estilo", "texto": "¿Qué estilo te define mejor?", "opciones": ["Elegante", "Deportivo", "Romántico"]},
    {"clave": "actividad", "texto": "¿Qué actividad disfrutas más?", "opciones": ["Salir de noche", "Viajar", "Leer un libro"]},
    {"clave": "clima", "texto": "¿Qué clima prefieres?", "opciones": ["Cálido", "Frío", "Templado"]},
    {"clave": "intensidad", "texto": "¿Qué intensidad de aroma prefieres?", "opciones": ["Suave", "Moderado", "Intenso"]},
    {"clave": "momento", "texto": "¿Para qué momento la usarías?", "opciones": ["Día", "Noche", "Ambos"]},
]

# Ajustar preguntas para regalo
def ajustar_preguntas_para_regalo(preguntas, nombre):
    preguntas_regalo = []
    for p in preguntas:
        p_nueva = p.copy()
        p_nueva["texto"] = p_nueva["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}").replace("¿Qué", f"¿Cuál")
        preguntas_regalo.append(p_nueva)
    return preguntas_regalo

# Inicialización del estado de la app
if "step" not in st.session_state:
    st.session_state.step = 0  # Paso inicial
if "sexo" not in st.session_state:
    st.session_state.sexo = None
if "para_regalo" not in st.session_state:
    st.session_state.para_regalo = None
if "nombre_regalo" not in st.session_state:
    st.session_state.nombre_regalo = None
if "pregs" not in st.session_state:
    st.session_state.pregs = []
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "chat" not in st.session_state:
    st.session_state.chat = []

# Función para agregar mensajes a la conversación
def add_message(sender, message):
    st.session_state.chat.append({"sender": sender, "message": message})

st.title("💬 Chatbot Coppel - Test de Fragancias")

# Mostrar la conversación
for msg in st.session_state.chat:
    if msg["sender"] == "bot":
        st.markdown(f"**Bot:** {msg['message']}")
    else:
        st.markdown(f"**Tú:** {msg['message']}")

# Paso 0: Preguntar si es para ti o para regalar
if st.session_state.step == 0:
    st.markdown("¿La fragancia es para ti o para regalar?")
    opcion = st.radio("Selecciona:", ["Para mí", "Para regalar"], key="opcion_0")
    if st.button("Enviar", key="btn_0"):
        add_message("user", opcion)
        st.session_state.para_regalo = opcion
        if opcion == "Para regalar":
            st.session_state.step = 0.5
        else:
            st.session_state.step = 1
            st.session_state.sexo = None  # Pediremos sexo para filtrar fragancias

        st.experimental_rerun()

# Paso 0.5: Preguntar nombre si es regalo
elif st.session_state.step == 0.5:
    nombre = st.text_input("¿Cómo se llama la persona a la que vas a regalar la fragancia?", key="input_nombre")
    if st.button("Enviar", key="btn_nombre"):
        if nombre.strip() == "":
            st.warning("Por favor ingresa un nombre.")
        else:
            add_message("user", nombre)
            st.session_state.nombre_regalo = nombre
            # Ajustar preguntas para regalo
            st.session_state.pregs = ajustar_preguntas_para_regalo(preguntas_base, nombre)
            st.session_state.step = 1
            st.session_state.sexo = None  # Pediremos sexo para filtrar fragancias
            st.experimental_rerun()

# Paso 1: Preguntar sexo para filtrar fragancias
elif st.session_state.step == 1:
    st.markdown("¿Cuál es tu sexo?")
    sexo = st.radio("Selecciona:", ["Masculino", "Femenino", "Otro / Prefiero no decir"], key="sexo")
    if st.button("Enviar", key="btn_sexo"):
        add_message("user", sexo)
        if sexo == "Masculino":
            st.session_state.sexo = "M"
        elif sexo == "Femenino":
            st.session_state.sexo = "F"
        else:
            st.session_state.sexo = "U"
        # Preparar preguntas si no es regalo
        if st.session_state.para_regalo == "Para mí":
            st.session_state.pregs = preguntas_base
        st.session_state.step = 2
        st.experimental_rerun()

# Paso 2 en adelante: Preguntar preguntas de la encuesta
elif st.session_state.step >= 2:
    idx = st.session_state.step - 2
    preguntas = st.session_state.pregs

    if idx < len(preguntas):
        p = preguntas[idx]
        st.markdown(f"**Bot:** {p['texto']}")
        opcion = st.radio("Selecciona:", p["opciones"], key=f"preg_{idx}")

        if st.button("Enviar", key=f"btn_preg_{idx}"):
            add_message("user", opcion)
            st.session_state.respuestas[p["clave"]] = opcion
            st.session_state.step += 1
            st.experimental_rerun()
    else:
        # Terminar encuesta y mostrar resultado
        respuestas = st.session_state.respuestas
        nombre = st.session_state.nombre_regalo if st.session_state.para_regalo == "Para regalar" else "tú"

        descripcion = (f"\n¡Gracias! Según tus respuestas, {nombre} disfruta del ambiente "
                       f"{respuestas.get('ambiente', '').lower()}, con un estilo "
                       f"{respuestas.get('estilo', '').lower()}, y prefiere fragancias de intensidad "
                       f"{respuestas.get('intensidad', '').lower()}. Ideal para momentos de "
                       f"{respuestas.get('actividad', '').lower()}.")

        # Filtrar catálogo según sexo
        sexo_usuario = st.session_state.sexo
        if sexo_usuario in ["M", "F"]:
            catalogo_filtrado = catalogo[catalogo["Sexo"].str.upper() == sexo_usuario]
        else:
            catalogo_filtrado = catalogo  # Si no especifica, sin filtro

        if catalogo_filtrado.empty:
            st.error("No se encontraron fragancias para tu selección de sexo.")
        else:
            recomendacion = catalogo_filtrado.sample(1).iloc[0]

            producto = recomendacion["C_producto"]
            precio = recomendacion["C_precio_descuento"]
            precio_original = recomendacion["C_precio_original"]
            descuento = precio_original - precio

            st.markdown(f"**Bot:** {descripcion}")
            st.markdown(f"**Bot:** Te recomendamos la siguiente fragancia: **{producto}**")
            st.markdown(f"Precio original: ${precio_original:.2f}")
            st.markdown(f"Precio en línea: ${precio:.2f} (ahorras ${descuento:.2f})")

        if st.button("Reiniciar encuesta"):
            st.session_state.step = 0
            st.session_state.sexo = None
            st.session_state.para_regalo = None
            st.session_state.nombre_regalo = None
            st.session_state.pregs = []
            st.session_state.respuestas = {}
            st.session_state.chat = []
            st.experimental_rerun()

