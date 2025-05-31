import pandas as pd
import random

# Carga catálogo de fragancias
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

def ajustar_preguntas_para_regalo(preguntas, nombre):
    preguntas_regalo = []
    for p in preguntas:
        p_nueva = p.copy()
        p_nueva["texto"] = p_nueva["texto"].replace("tu", f"de {nombre}").replace("Te", f"{nombre}").replace("¿Qué", "¿Cuál")
        preguntas_regalo.append(p_nueva)
    return preguntas_regalo

def chatbot():
    print("¿La fragancia es para ti o para regalar?")
    opcion = input("1. Para mí\n2. Para regalar\nSelecciona (1 o 2): ").strip()
    if opcion == "1":
        nombre = "ti"
        preguntas = preguntas_base
    elif opcion == "2":
        nombre = input("¿Cómo se llama la persona a la que vas a regalar la fragancia?: ").strip()
        preguntas = ajustar_preguntas_para_regalo(preguntas_base, nombre)
    else:
        print("Opción no válida.")
        return
    
    respuestas = {}
    for p in preguntas:
        print(f"\n{p['texto']}")
        for idx, o in enumerate(p["opciones"], 1):
            print(f"{idx}. {o}")
        while True:
            seleccion = input("Selecciona (1, 2 o 3): ").strip()
            if seleccion in ["1", "2", "3"]:
                break
            print("Opción inválida, intenta de nuevo.")
        respuestas[p["clave"]] = p["opciones"][int(seleccion)-1]
    
    # Descripción personalizada
    descripcion = (f"\n¡Gracias! Según tus respuestas, {'eres' if opcion == '1' else f'{nombre} es'} alguien que disfruta del ambiente {respuestas['ambiente'].lower()}, "
                   f"con un estilo {respuestas['estilo'].lower()}, y prefiere fragancias de intensidad {respuestas['intensidad'].lower()}. Ideal para momentos de {respuestas['actividad'].lower()}.")
    print(descripcion)
    
    # Recomendación aleatoria
    recomendacion = catalogo.sample(1).iloc[0]
    producto = recomendacion["C_producto"]
    precio_original = recomendacion["C_precio_original"]
    precio_descuento = recomendacion["C_precio_descuento"]
    descuento = precio_original - precio_descuento
    
    print(f"\nTe recomendamos la siguiente fragancia: {producto}")
    print(f"Precio original: ${precio_original:.2f}")
    print(f"Precio en línea: ${precio_descuento:.2f} (ahorras ${descuento:.2f})")

# Ejecutar el chatbot
chatbot()






