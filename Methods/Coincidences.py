import json
from collections import Counter

# Cargar palabras clave desde un archivo JSON externo
with open("../Data/KeyWords/keyWords.json", "r", encoding="utf-8") as f:
    palabras_clave = json.load(f)

# Leer los tokens guardados desde el archivo de texto
with open("../Data/tokens.txt", "r", encoding="utf-8") as f:
    todos_los_tokens = f.read().splitlines()

# Contar ocurrencias de cada token
conteo_tokens = Counter(todos_los_tokens)

coincidencias = []

# Recorrer cada categoría y sus palabras
for categoria, lista_palabras in palabras_clave.items():
    for palabra in lista_palabras:
        cantidad = conteo_tokens.get(palabra, 0)
        coincidencias.append((palabra, cantidad, categoria))

# Mostrar todas las palabras, con o sin coincidencias
for palabra, cantidad, categoria in coincidencias:
    print(f"{palabra}: {cantidad} apariciones (Categoría: {categoria})")