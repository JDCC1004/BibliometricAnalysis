import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def get_vector_paths():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    matrices_dir = os.path.join(root_dir, 'Data', 'Matrices')
    abstracts_path = os.path.join(root_dir, 'Data', 'Abstracts', 'abstracts_limpios.csv')
    return {
        "tfidf": os.path.join(matrices_dir, 'tfidf_vector_matrix.npy'),
        "bert": os.path.join(matrices_dir, 'bert_vector_matrix.npy'),
        "abstracts": abstracts_path
    }


def load_vector_matrices(paths):
    try:
        tfidf = np.load(paths["tfidf"])
        bert = np.load(paths["bert"])
        print("Vectores cargados exitosamente.")
        return tfidf, bert
    except FileNotFoundError:
        print("Error: Asegúrate de que los archivos .npy existan en la carpeta Data/Matrices.")
        exit()


def apply_kmeans(vectors, n_clusters, name="Modelo"):
    print(f"\nAplicando K-Means con k={n_clusters} a los vectores {name}...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(vectors)
    print(f"K-Means con {name} completado.")
    return labels, kmeans


def show_cluster_assignments(labels, name):
    print(f"Asignación de clústeres para los primeros 10 abstracts ({name}):")
    print(labels[:10])


def evaluate_clustering(vectors, labels, name):
    try:
        score = silhouette_score(vectors, labels)
        print(f"Silhouette Score para K-Means ({name}): {score:.4f}")
    except Exception as e:
        print(f"No se pudo calcular el Silhouette Score para {name}: {e}")


def kmeans_clustering():
    n_clusters = 5
    paths = get_vector_paths()
    tfidf_vectors, bert_vectors = load_vector_matrices(paths)

    tfidf_labels, _ = apply_kmeans(tfidf_vectors, n_clusters, "TF-IDF")
    bert_labels, _ = apply_kmeans(bert_vectors, n_clusters, "BERT")

    print("\nResultados de K-Means:")
    show_cluster_assignments(tfidf_labels, "TF-IDF")
    show_cluster_assignments(bert_labels, "BERT")

    print("\nEvaluación de los clústeres:")
    evaluate_clustering(tfidf_vectors, tfidf_labels, f"TF-IDF, k={n_clusters}")
    evaluate_clustering(bert_vectors, bert_labels, f"BERT, k={n_clusters}")
