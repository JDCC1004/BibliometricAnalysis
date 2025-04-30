import os
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Crear carpeta de salida
os.makedirs("../Graphics/WordCloud", exist_ok=True)

# Ruta donde están las tablas
carpeta_tablas = "../Tables"

# Recorrer archivos de texto
for archivo in os.listdir(carpeta_tablas):
    if archivo.endswith(".txt"):
        ruta = os.path.join(carpeta_tablas, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()

        # Extraer tuplas (palabra, frecuencia) ignorando encabezados y bordes
        matches = re.findall(r"│ ([^│]+?)\s+│\s+(\d+)\s+│", texto)
        datos = {palabra.strip(): int(frecuencia) for palabra, frecuencia in matches}

        if not datos:
            continue  # Saltar si está vacío

        # Crear WordCloud
        wc = WordCloud(width=1000, height=500, background_color="white", colormap="viridis")
        wc.generate_from_frequencies(datos)

        # Guardar imagen
        nombre_categoria = archivo.replace(".txt", "")
        ruta_salida = f"../Graphics/WordClod/{nombre_categoria}.png"
        wc.to_file(ruta_salida)


print("✅ Nubes de palabras generadas en la carpeta 'nubes/'")
