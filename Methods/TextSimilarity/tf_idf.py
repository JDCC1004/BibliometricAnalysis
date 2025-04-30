import nltk
import pandas as pd
import os
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def eliminar_stopwords(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s.,;:()\-]", '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    word = text.split()
    filtered_words = [word for word in word if word not in stop_words]
    return ' '.join(filtered_words)


def mount_csv():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(root_dir, 'Data', 'Abstracts', 'abstracts_limpios.csv')

    # Cargar el CSV
    df = pd.read_csv(csv_path, encoding='utf-8')

    print(f"Número de abstracts cargados: {len(df)}")
    df['abstract'] = df['abstract'].apply(eliminar_stopwords)
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


def export_matrix(cosine_matrix):

    # Guardar la matriz de similitud
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(root_dir, 'Data', 'Matrices', 'tfidf_cosine_sim_matrix.npy')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Añadir esta línea para asegurar que sea un array NumPy de tipo float
    cosine_sim_matrix_np = np.array(cosine_matrix, dtype=np.float64)

    # Guardar el array explícitamente convertido
    np.save(output_path, cosine_sim_matrix_np)
    print(f"Matriz de similitud TF-IDF guardada (conversión explícita a float64) en: {output_path}")


def export_vector_matrix(tfidf_matrix):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(root_dir, 'Data', 'Matrices', 'tfidf_vector_matrix.npy')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    tfidf_array = tfidf_matrix.toarray()  # Convertir matriz dispersa a densa
    np.save(output_path, tfidf_array)
    print(f"Matriz de vectores TF-IDF guardada en: {output_path}")


def tfidf():

    df = mount_csv() # ---> Cargar el CSV con los abstracts limpios
    tfidf_matrix = vectorise(df) # ---> Vectorizar los abstracts usando TF-IDF
    cosine_sim_matrix = cosine_sim(tfidf_matrix)  # ---> Calcular la matriz de similitud coseno
    export_matrix(cosine_sim_matrix)  # ---> Guardar la matriz de similitud
    export_vector_matrix(tfidf_matrix)  # ---> Guardar la matriz de vectores TF-IDF



    #------------------------------ Verificación de la similitud - Ejemplo --------------------------------
    # Obtener las similitudes del abstract 0
    sim_scores = list(enumerate(cosine_sim_matrix[0]))

    # Ordenar de mayor a menor similitud (excluyendo el mismo abstract)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]  # El primer valor es el mismo abstract (similitud 1.0)

    # Mostrar los 5 más similares
    print("Top 5 abstracts más similares al abstract 0:")
    for idx, score in sim_scores[:5]:
        print(f"Abstract {idx} con similitud {score:.4f}")


if __name__ == "__main__":
    tfidf()