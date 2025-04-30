from Coincidences import coincidencias
from tabulate import tabulate
import os

# Crear carpeta 'tablas' si no existe
os.makedirs("../Tables", exist_ok=True)

# Ordenamiento con timsort
def criterio(item):
    return item[1]

def timsort(data):
    return sorted(data, key=criterio, reverse=True)

# Agrupar por categoría
categorias = {}
for palabra, frecuencia, categoria in coincidencias:
    categorias.setdefault(categoria, []).append((palabra, frecuencia))

# Procesar por categoría
for categoria, items in categorias.items():
    ordenados = timsort(items)
    tabla = tabulate(ordenados, headers=["Palabra Clave", "Frecuencia"], tablefmt="fancy_grid")

    # Mostrar en consola
    print(f"\nCategoría: {categoria}")
    print(tabla)

    # Guardar en archivo
    output_path = f"../Tables/{categoria}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Categoría: {categoria}\n")
        f.write(tabla)

print("✅ Tablas por categoría exportadas en formato 'fancy_grid' en la carpeta 'tablas/'")
