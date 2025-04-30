import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import os
import torch
from sentence_transformers.util import cos_sim


def mount_csv():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(root_dir, 'Data', 'Abstracts', 'abstracts_limpios.csv')

    # Cargar
    df = pd.read_csv(csv_path, encoding='utf-8')

    print(f"Número de abstracts cargados: {len(df)}")
    return df

def vectorise(df):
    # Cargar modelo BERT optimizado para similitud semántica
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Rápido y efectivo

    # Codificar los abstracts
    embeddings = model.encode(df['abstract'].tolist(), convert_to_tensor=True)

    print(f"Shape de los embeddings: {embeddings.shape}")
    return embeddings

def similarity(embeddings):
    # Calcular similitud coseno entre todos los abstracts
    cosine_sim_matrix = cos_sim(embeddings, embeddings)

    print(f"Shape de la matriz de similitud: {cosine_sim_matrix.shape}")
    return cosine_sim_matrix

def export_matrix(cosine_matrix):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(root_dir, 'Data', 'Matrices', 'bert_cosine_sim_matrix.npy')
    # Asegurar que el directorio 'Matrices' exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, cosine_matrix.numpy())
    print(f"Matriz de similitud BERT guardada en: {output_path}")


def export_embeddings(embeddings):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(root_dir, 'Data', 'Matrices', 'bert_vector_matrix.npy')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    np.save(output_path, embeddings.cpu().numpy())  # Convertir a NumPy y exportar
    print(f"Embeddings BERT guardados en: {output_path}")

def bert():

    df = mount_csv() # ---> Cargar el CSV con los abstracts limpios
    embedding = vectorise(df)  # ---> Vectorizar los abstracts usando BERT
    cosine_matrix = similarity(embedding)  # ---> Calcular la matriz de similitud coseno
    export_matrix(cosine_matrix) # ---> Guardar la matriz de similitud
    export_embeddings(embedding) # ---> Guardar los embeddings



    # ----------------------- Ejemplo de uso -----------------------
    similarities = cosine_matrix[0]
    top_results = torch.topk(similarities, k=6)  # top 6 (incluye el mismo)

    print("Abstractos más similares al abstract 0:")
    for score, idx in zip(top_results.values[1:], top_results.indices[1:]):  # [1:] para omitir el mismo
        print(f"Abstract {idx.item()} con similitud {score.item():.4f}")

    return  cosine_matrix

if __name__ == "__main__":
    bert()

