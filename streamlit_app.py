import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recomendador de Fragancias", layout="centered")
st.title("💐 Test de fragancias")

# Cargar archivo Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("fragancias_recomendadas.xlsx")
    df.columns = df.columns.str.strip().str.lower()  # normalizar nombres
    return df

df = cargar_datos()

# Preguntas
sexo = st.radio("1. ¿Cuál es tu sexo?", ["Hombre", "Mujer", "Prefiero no decirlo"])
ambiente = st.selectbox("2. ¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"])
estilo = st.selectbox("3. ¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"])
actividad = st.selectbox("4. ¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"])
clima = st.selectbox("5. ¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"])
intensidad = st.selectbox("6. ¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"])
momento = st.selectbox("7. ¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"])

# Botón para recomendar
if st.button("🎯 Ver mis fragancias ideales"):
    resultados = df[
        (df['sexo'] == sexo.lower()) &
        (df['ambiente'] == ambiente.lower()) &
        (df['estilo'] == estilo.lower()) &
        (df['actividad'] == actividad.lower()) &
        (df['clima'] == clima.lower()) &
        (df['intensidad'] == intensidad.lower()) &
        (df['momento'] == momento.lower())
    ]

    if not resultados.empty:
        st.success("🌟 Estas son tus fragancias recomendadas:")
        top3 = resultados.sample(n=min(3, len(resultados)), random_state=42)
        st.table(top3[['fragancia', 'precio', 'precio final']])
    else:
        st.warning("😔 No encontramos coincidencias exactas. Prueba con otras combinaciones.")
