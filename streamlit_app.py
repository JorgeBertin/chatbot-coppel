import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Recomendador de Fragancias", layout="centered")
st.title("Recomendador de Fragancias - Coppel")

# Subida del archivo
archivo_excel = st.file_uploader("📂 Sube tu catálogo de fragancias (.xlsx)", type="xlsx")

if archivo_excel is not None:
    # Cargar y limpiar los datos directamente
    df = pd.read_excel(archivo_excel)
    df.columns = df.columns.str.strip()  # Elimina espacios en nombres de columnas

    # Normalizar columnas relevantes
    columnas_a_normalizar = ["Sexo", "Ambiente", "Estilo", "Actividad", "Clima", "Intensidad", "Momento"]
    for col in columnas_a_normalizar:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Preguntas
    sexo = st.selectbox("¿Cuál es tu sexo?", ["Femenino", "Masculino", "Prefiero no decirlo"]).lower()
    ambiente = st.selectbox("¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"]).lower()
    estilo = st.selectbox("¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"]).lower()
    actividad = st.selectbox("¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"]).lower()
    clima = st.selectbox("¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"]).lower()
    intensidad = st.selectbox("¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"]).lower()
    momento = st.selectbox("¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"]).lower()

    if st.button("🔍 Recomendar fragancias"):
        filtros = (
            ((df['sexo'] == sexo) | (sexo == "prefiero no decirlo")) &
            (df['ambiente'] == ambiente) &
            (df['estilo'] == estilo) &
            (df['actividad'] == actividad) &
            (df['clima'] == clima) &
            (df['intensidad'] == intensidad) &
            (df['momento'] == momento)
        )

        resultados = df[filtros]

        if len(resultados) >= 3:
            seleccion = resultados.sample(3)
        elif len(resultados) > 0:
            seleccion = resultados.sample(len(resultados))
        else:
            seleccion = df.sample(3)
            st.warning("😔 No se encontraron coincidencias exactas. Aquí tienes recomendaciones generales:")

        for idx, row in seleccion.iterrows():
            st.markdown(f"""
            **{row['Nombre']}**
            - Sexo: {row['Sexo']}
            - Estilo: {row['Estilo']}
            - Intensidad: {row['Intensidad']}
            - Clima: {row['Clima']}
            - Precio: ${row['Precio']}
            """)
else:
    st.info("Por favor, sube un archivo Excel con tu catálogo para comenzar.")




