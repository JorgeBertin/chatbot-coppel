import gradio as gr
import pandas as pd
import random

df = pd.read_excel("catalogo_fragancias.xlsx")

def recomendar(sexo, ambiente, estilo, actividad, clima, intensidad, momento):
    filtros = (
        (df['Sexo'].str.lower() == sexo.lower()) |
        (sexo == "Prefiero no decirlo")
    ) & (df['Ambiente'] == ambiente) & (df['Estilo'] == estilo) & \
        (df['Actividad'] == actividad) & (df['Clima'] == clima) & \
        (df['Intensidad'] == intensidad) & (df['Momento'] == momento)

    resultados = df[filtros]
    if len(resultados) >= 3:
        seleccion = resultados.sample(3)
    elif len(resultados) > 0:
        seleccion = resultados.sample(len(resultados))
    else:
        seleccion = df.sample(3)

    return "\n\n".join([f"{row['Nombre']} - {row['Precio']}" for _, row in seleccion.iterrows()])

iface = gr.Interface(
    fn=recomendar,
    inputs=[
        gr.Dropdown(["Femenino", "Masculino", "Prefiero no decirlo"], label="Sexo"),
        gr.Dropdown(["Bosque", "Playa", "Ciudad"], label="Ambiente"),
        gr.Dropdown(["Elegante", "Deportivo", "Romántico"], label="Estilo"),
        gr.Dropdown(["Salir de noche", "Viajar", "Leer un libro"], label="Actividad"),
        gr.Dropdown(["Cálido", "Frío", "Templado"], label="Clima"),
        gr.Dropdown(["Suave", "Moderado", "Intenso"], label="Intensidad"),
        gr.Dropdown(["Día", "Noche", "Ambos"], label="Momento")
    ],
    outputs="text",
    title="Recomendador de Fragancias"
)

iface.launch()

