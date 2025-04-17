import re
import string

# Rutas de archivos
archivo_bib = "../Data/BasesUnificadas.bib"
archivo_frases = "compuestas.txt"

# Leer el contenido del archivo .bib
with open(archivo_bib, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

# Extraer abstracts usando regex
abstracts = re.findall(r'abstract\s*=\s*[{"](.+?)[}"]', contenido, re.IGNORECASE | re.DOTALL)

# Leer frases clave y convertir a minúsculas
with open(archivo_frases, "r", encoding="utf-8") as f:
    frases = [line.strip().lower() for line in f if line.strip()]

todos_los_tokens = []

for abstract in abstracts:
    abstract = abstract.lower()  # Convertir abstract a minúsculas

    # Reemplazar frases compuestas
    for frase in frases:
        palabras = frase.split()
        patron = r'\b' + r'[\s\.,;:"\'()\[\]{}!?-]*'.join(map(re.escape, palabras)) + r'\b'

        if re.search(patron, abstract, flags=re.IGNORECASE):
            print(f"[✔] Reemplazando '{frase}' → '{frase.replace(' ', '_')}' en abstract.")

        abstract = re.sub(patron, frase.replace(" ", "_"), abstract, flags=re.IGNORECASE)

    # Eliminar puntuación (excepto guiones bajos)
    abstract_limpio = abstract.translate(str.maketrans('', '', string.punctuation.replace("_", "")))

    # Tokenizar y agregar al conjunto global
    tokens = abstract_limpio.split()
    todos_los_tokens.extend(tokens)

# Guardar tokens en un archivo
with open("tokens.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(todos_los_tokens))

# Verificación de la frase 'mobile_application'
with open("tokens.txt", "r", encoding="utf-8") as f:
    tokens = f.read().splitlines()
