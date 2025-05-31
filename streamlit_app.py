import streamlit as st
import pandas as pd
import random

# Título
st.title("Recomendador de Fragancias - Coppel")

# Cargar catálogo
@st.cache_data
def cargar_datos():
    return pd.read_excel("catalogo_fragancias.xlsx")

df = cargar_datos()

# Preguntas al usuario
sexo = st.selectbox("¿Cuál es tu sexo?", ["Femenino", "Masculino", "Prefiero no decirlo"])
ambiente = st.selectbox("¿Cuál es tu ambiente favorito?", ["Bosque", "Playa", "Ciudad"])
estilo = st.selectbox("¿Qué estilo te define mejor?", ["Elegante", "Deportivo", "Romántico"])
actividad = st.selectbox("¿Qué actividad disfrutas más?", ["Salir de noche", "Viajar", "Leer un libro"])
clima = st.selectbox("¿Qué clima prefieres?", ["Cálido", "Frío", "Templado"])
intensidad = st.selectbox("¿Qué intensidad de aroma prefieres?", ["Suave", "Moderado", "Intenso"])
momento = st.selectbox("¿Para qué momento la usarías?", ["Día", "Noche", "Ambos"])

# Botón para recomendar
if st.button("Recomendar fragancias"):
    # Filtrar catálogo según las respuestas
    filtros = (
        (df['Sexo'].str.lower() == sexo.lower()) |
        (sexo == "Prefiero no decirlo")
    ) & (df['Ambiente'] == ambiente) \
      & (df['Estilo'] == estilo) \
      & (df['Actividad'] == actividad) \
      & (df['Clima'] == clima) \
      & (df['Intensidad'] == intensidad) \
      & (df['Momento'] == momento)

    recomendaciones = df[filtros]

    if len(recomendaciones) >= 3:
        seleccion = recomendaciones.sample(3)
    elif len(recomendaciones) > 0:
        seleccion = recomendaciones.sample(len(recomendaciones))
    else:
        seleccion = df.sample(3)
        st.warning("No se encontraron coincidencias exactas. Estas son recomendaciones generales:")

    # Mostrar recomendaciones
    for idx, row in seleccion.iterrows():
        st.markdown(f"""
        **{row['Nombre']}**
        - Sexo: {row['Sexo']}
        - Estilo: {row['Estilo']}
        - Intensidad: {row['Intensidad']}
        - Clima: {row['Clima']}
        - Precio: ${row['Precio']}
        """)



