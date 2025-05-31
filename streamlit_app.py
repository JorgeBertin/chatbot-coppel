import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recomendador de Fragancias", layout="centered")
st.title("💐 Test de fragancias")

# Cargar archivo Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("fragancias_hombre_mujer.xlsx")
    return df

df = cargar_datos()

# Preguntas
sexo = st.radio("1. ¿Cuál es tu sexo?", ["Masculino", "Femenino", "Prefiero no decirlo"])
ambiente = st.selectbox("2. ¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"])
estilo = st.selectbox("3. ¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"])
actividad = st.selectbox("4. ¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"])
clima = st.selectbox("5. ¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"])
intensidad = st.selectbox("6. ¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"])
momento = st.selectbox("7. ¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"])

# Botón
if st.button("🎯 Ver mis fragancias ideales"):
    # Filtrar DataFrame según respuestas
    resultados = df[
        (df['Sexo'].str.lower() == sexo.lower()) &
        (df['Ambiente'].str.lower() == ambiente.lower()) &
        (df['Estilo'].str.lower() == estilo.lower()) &
        (df['Actividad'].str.lower() == actividad.lower()) &
        (df['Clima'].str.lower() == clima.lower()) &
        (df['Intensidad'].str.lower() == intensidad.lower()) &
        (df['Momento'].str.lower() == momento.lower())
    ]

    if not resultados.empty:
        st.success("🌟 Estas son tus fragancias recomendadas:")
        top3 = resultados.sample(n=min(3, len(resultados)), random_state=42)
        st.table(top3[['Fragancia']])  # Cambia esto si quieres mostrar más columnas
    else:
        st.warning("😔 No encontramos coincidencias exactas. Prueba con otras combinaciones o ajusta el archivo de datos.")
