# Mostrar todo el historial tipo chat (solo mensajes de usuario y mensajes finales de bot)
st.title("💬 Chatbot Coppel")
for author, msg in st.session_state.history:
    with st.chat_message(author):
        st.markdown(msg)

# --- STEP 0: Pregunta inicial ---
if st.session_state.step == 0:
    pregunta_inicial = "¿La fragancia es para ti o para regalar?"
    st.markdown(f"**Bot:** {pregunta_inicial}")
    opcion = st.radio("Selecciona:", ["Para mí", "Para regalar"], key="opt0")
    if st.button("Enviar", key="btn0"):
        add_message("user", opcion)
        if opcion == "Para mí":
            st.session_state.nombre = "ti"
            st.session_state.pregs = preguntas_base
            st.session_state.step = 1
        else:
            st.session_state.step = -1

# --- STEP -1: Si es regalo, pedimos nombre ---
elif st.session_state.step == -1:
    pregunta_nombre = "¿Cómo se llama la persona a la que vas a regalar la fragancia?"
    st.markdown(f"**Bot:** {pregunta_nombre}")
    nombre = st.text_input("Nombre del destinatario")
    if st.button("Enviar", key="btn_name") and nombre.strip():
        add_message("user", nombre.strip())
        st.session_state.nombre = nombre.strip()
        st.session_state.pregs = ajustar_para_regalo(preguntas_base, nombre.strip())
        st.session_state.step = 1

# --- STEPS 1..N: Preguntas de la encuesta ---
elif 1 <= st.session_state.step <= len(st.session_state.pregs):
    idx = st.session_state.step - 1
    preg = st.session_state.pregs[idx]

    # Mostrar pregunta (texto arriba del input)
    st.markdown(f"**Bot:** {preg['texto']}")

    choice = st.radio("", preg["opciones"], key=f"opt{idx}")
    if st.button("Enviar", key=f"btn{idx}"):
        add_message("user", choice)
        st.session_state.respuestas[preg["clave"]] = choice
        st.session_state.step += 1

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






