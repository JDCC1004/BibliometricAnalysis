import os

import bibtexparser
import pandas as pd
import re

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Metodo que extrae el ID, el título y el abstract de un archivo bibtex y lo guarda en un archivo CSV
def extract():

    bibtex_file_path = 'Data/BasesFiltradas.bib'

    with open(bibtex_file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    entries = bib_database.entries

    data = []
    for idx, entry in enumerate(entries):
        entry_id = entry.get('ID', None)

        # Si no tiene ID, crear uno basado en el índice
        if not entry_id:
            entry_id = f'entry_{idx}'

        title = entry.get('title', '').strip()
        abstract = entry.get('abstract', '').strip()

        # Solo guardar citas que tienen abstract
        if abstract:
            data.append({
                'id': entry_id,
                'title': title,
                'abstract': abstract
            })

    df = pd.DataFrame(data)

    csv_output_path = 'Data/Abstracts/abstracts_extraidos.csv'
    df.to_csv(csv_output_path, index=False, encoding='utf-8')
    print(f'¡Datos extraídos y guardados exitosamente en: {csv_output_path}!')

def limpiar_texto(texto):

    texto = str(texto)
    texto = texto.lower()
    # Eliminar caracteres raros, dejando letras, números y algunos signos útiles
    texto = re.sub(r"[^a-zA-Z0-9\s.,;:()\-]", '', texto)

    # Eliminar espacios duplicados
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def normalize():
    #Cargar el CSV con los abstracts
    csv_path = os.path.join(root_dir, 'Data', 'Abstracts', 'abstracts_extraidos.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')

    # Filtrar las columnas que no contengan abstract
    df = df.dropna(subset=['abstract'])
    df = df[df['abstract'].str.strip() != '']

    df['abstract'] = df['abstract'].apply(limpiar_texto)

    clean_csv_path = os.path.join(root_dir, 'Data', 'Abstracts', "abstracts_limpios.csv")
    df.to_csv(clean_csv_path, index=False, encoding='utf-8')
    print(f'Abstracts limpiados y guardados en {clean_csv_path}')


def main():
    normalize()


if __name__ == "__main__":
    main()