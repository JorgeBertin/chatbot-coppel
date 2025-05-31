import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recomendador de Fragancias", layout="centered")
st.title("💐 Test de fragancias")

# Cargar archivo Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("fragancias_recomendadas.xlsx")
    df.columns = df.columns.str.strip().str.lower()  # nombres de columna
    columnas_objetivo = ["sexo", "ambiente", "estilo", "actividad", "clima", "intensidad", "momento"]
    for col in columnas_objetivo:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df

df = cargar_datos()

# Preguntas al usuario
sexo = st.radio("1. ¿Cuál es tu sexo?", ["Masculino", "Femenino", "Prefiero no decirlo"]).lower()
ambiente = st.selectbox("2. ¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"]).lower()
estilo = st.selectbox("3. ¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"]).lower()
actividad = st.selectbox("4. ¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"]).lower()
clima = st.selectbox("5. ¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"]).lower()
intensidad = st.selectbox("6. ¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"]).lower()
momento = st.selectbox("7. ¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"]).lower()

# Botón para recomendar
if st.button("🎯 Ver mis fragancias ideales"):
    filtros = (
        (df['sexo'] == sexo) &
        (df['ambiente'] == ambiente) &
        (df['estilo'] == estilo) &
        (df['actividad'] == actividad) &
        (df['clima'] == clima) &
        (df['intensidad'] == intensidad) &
        (df['momento'] == momento)
    )

    resultados = df[filtros]

    if not resultados.empty:
        st.success("🌟 Estas son tus fragancias recomendadas:")
        top3 = resultados.sample(n=min(3, len(resultados)), random_state=42)
        st.table(top3[['fragancia', 'precio', 'precio final']])
    else:
        st.warning("😔 No encontramos coincidencias exactas. Aquí tienes sugerencias por tipo:")
        if sexo in ["masculino", "femenino"]:
            respaldo = df[df["sexo"] == sexo]
        else:
            respaldo = df.copy()

        if respaldo.empty:
            st.error("No hay fragancias disponibles en el catálogo.")
        else:
            top3 = respaldo.sample(n=min(3, len(respaldo)), random_state=42)
            st.table(top3[['fragancia', 'precio', 'precio final']])





