import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Recomendador de Fragancias", layout="centered")
st.title("💐 Test de fragancias")

# Cargar archivo Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("fragancias_recomendadas.xlsx")
    df.columns = df.columns.str.strip().str.lower()  # normalizar nombres de columna
    if 'sexo' in df.columns:
        df['sexo'] = df['sexo'].astype(str).str.strip().str.lower()
    return df

df = cargar_datos()

# Preguntas al usuario (no se usan para filtrar, excepto sexo)
sexo = st.radio("1. ¿Cuál es tu sexo?", ["Masculino", "Femenino", "Prefiero no decirlo"]).lower()
ambiente = st.selectbox("2. ¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"])
estilo = st.selectbox("3. ¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"])
actividad = st.selectbox("4. ¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"])
clima = st.selectbox("5. ¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"])
intensidad = st.selectbox("6. ¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"])
momento = st.selectbox("7. ¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"])

# Botón para recomendar
if st.button("🎯 Ver mi fragancia ideal"):
    # Filtrar solo por sexo
    if sexo in ["masculino", "femenino"]:
        resultados = df[df['sexo'] == sexo]
    else:
        resultados = df

    if not resultados.empty:
        seleccion = resultados.sample(1, random_state=random.randint(0, 10000))
        st.success("🌟 Esta es tu fragancia ideal:")
        st.table(seleccion[['fragancia', 'precio', 'precio final']])
    else:
        st.warning("😔 No se encontraron fragancias disponibles.")
