import streamlit as st

st.set_page_config(page_title="Test de fragancias", layout="centered")

st.title("💐 Test de preferencias de fragancias")

# Preguntas
sexo = st.radio("1. ¿Cuál es tu sexo?", ["Masculino", "Femenino", "Prefiero no decirlo"])

ambiente = st.selectbox("2. ¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"])

estilo = st.selectbox("3. ¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"])

actividad = st.selectbox("4. ¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"])

clima = st.selectbox("5. ¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"])

intensidad = st.selectbox("6. ¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"])

momento = st.selectbox("7. ¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"])

# Botón para enviar
if st.button("Enviar respuestas"):
    st.success("✅ ¡Gracias por completar el test!")
    st.subheader("Tus respuestas:")
    st.write(f"- Sexo: {sexo}")
    st.write(f"- Ambiente favorito: {ambiente}")
    st.write(f"- Estilo: {estilo}")
    st.write(f"- Actividad favorita: {actividad}")
    st.write(f"- Clima preferido: {clima}")
    st.write(f"- Intensidad de aroma: {intensidad}")
    st.write(f"- Momento de uso: {momento}")
    
    # Aquí podrías agregar lógica para recomendar una fragancia o guardar los datos
