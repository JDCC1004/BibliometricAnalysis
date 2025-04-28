import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np



def mount_csv():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(root_dir, 'Data', 'Abstracts', 'abstracts_limpios.csv')

    # 2. Cargar el CSV
    df = pd.read_csv(csv_path, encoding='utf-8')

    # 3. Verificar
    print(f"Número de abstracts cargados: {len(df)}")
    print(df.head())
    return df

def vectorise(df):
    # Crear el vectorizador
    vectorizer = TfidfVectorizer(
        #stop_words='english',  # Eliminar stopwords en inglés (puedes quitarlo si tus abstracts están en español)
        ngram_range=(1, 2),  # Unigramas y bigramas (palabras y pares de palabras)
        max_features=5000  # Limitar el vocabulario a las 5000 palabras/pares más frecuentes (opcional)
    )

    # Aplicarlo a los abstracts
    tfidf_matrix = vectorizer.fit_transform(df['abstract'])

    print(f"Shape de la matriz TF-IDF: {tfidf_matrix.shape}")  # (n_abstracts, vocabulario)
    return tfidf_matrix


def cosine_sim(tfidf_matrix):
    # Calcular similitud coseno entre todos los abstracts
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print(f"Shape de la matriz de similitud: {cosine_sim_matrix.shape}")
    return cosine_sim_matrix


def tfidf():

    df = mount_csv() # ---> Cargar el CSV con los abstracts limpios
    tfidf_matrix = vectorise(df) # ---> Vectorizar los abstracts usando TF-IDF
    cosine_sim_matrix = cosine_sim(tfidf_matrix)

    #------------------------------ Verificación de la similitud --------------------------------
    # Obtener las similitudes del abstract 0
    sim_scores = list(enumerate(cosine_sim_matrix[69]))

    # Ordenar de mayor a menor similitud (excluyendo el mismo abstract)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]  # El primer valor es el mismo abstract (similitud 1.0)

    # Mostrar los 5 más similares
    print("Top 5 abstracts más similares al abstract 0:")
    for idx, score in sim_scores[:5]:
        print(f"Abstract {idx} con similitud {score:.4f}")

