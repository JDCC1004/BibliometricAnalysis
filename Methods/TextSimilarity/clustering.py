import numpy as np
import os
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


def get_matrices_paths():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    matrices_dir = os.path.join(root_dir, 'Data', 'Matrices')
    return {
        "tfidf_sim": os.path.join(matrices_dir, 'tfidf_cosine_sim_matrix.npy'),
        "bert_sim": os.path.join(matrices_dir, 'bert_cosine_sim_matrix.npy'),
        "tfidf_embed": os.path.join(matrices_dir, 'tfidf_vector_matrix.npy'),
        "bert_embed": os.path.join(matrices_dir, 'bert_vector_matrix.npy')
    }


def load_similarity_matrices(paths):
    try:
        tfidf_sim_matrix = np.load(paths["tfidf_sim"], allow_pickle=True)
        bert_sim_matrix = np.load(paths["bert_sim"], allow_pickle=True)
        print("Matrices de similitud cargadas exitosamente.")
        return tfidf_sim_matrix, bert_sim_matrix
    except FileNotFoundError:
        print("Error: Asegúrate de que los archivos .npy existan en la carpeta Data/Matrices.")
        exit()


def cosine_similarity_to_distance_matrix(sim_matrix):
    dist_matrix = 1 - sim_matrix
    np.fill_diagonal(dist_matrix, 0)
    return np.clip(dist_matrix, a_min=0, a_max=None)


def convert_to_condensed(matrix):
    upper_tri_indices = np.triu_indices(matrix.shape[0], k=1)
    return matrix[upper_tri_indices]


def perform_hierarchical_clustering(dist_condensed, method):
    print(f"Realizando agrupamiento jerárquico con criterio '{method}'...")
    return linkage(dist_condensed, method=method)


def plot_dendrogram(linkage_matrix, title):
    plt.figure(figsize=(12, 7))
    plt.title(title)
    plt.xlabel('Índice del Abstract')
    plt.ylabel('Distancia')
    dendrogram(linkage_matrix)
    plt.show()


def hierarchical_clustering():
    paths = get_matrices_paths()
    tfidf_sim, bert_sim = load_similarity_matrices(paths)

    tfidf_dist = cosine_similarity_to_distance_matrix(tfidf_sim)
    bert_dist = cosine_similarity_to_distance_matrix(bert_sim)
    print("Distancias negativas recortadas a 0.")

    tfidf_condensed = convert_to_condensed(tfidf_dist)
    bert_condensed = convert_to_condensed(bert_dist)

    # TF-IDF
    Z_tfidf_ward = perform_hierarchical_clustering(tfidf_condensed, 'ward')
    Z_tfidf_avg = perform_hierarchical_clustering(tfidf_condensed, 'average')

    # BERT
    Z_bert_ward = perform_hierarchical_clustering(bert_condensed, 'ward')
    Z_bert_avg = perform_hierarchical_clustering(bert_condensed, 'average')

    print("Agrupamiento jerárquico completado para todos los casos.")

    # Dendrogramas
    print("\nGenerando dendrogramas...")
    plot_dendrogram(Z_tfidf_ward, 'Dendrograma TF-IDF - Enlace Ward')
    plot_dendrogram(Z_tfidf_avg, 'Dendrograma TF-IDF - Enlace Average')
    plot_dendrogram(Z_bert_ward, 'Dendrograma BERT - Enlace Ward')
    plot_dendrogram(Z_bert_avg, 'Dendrograma BERT - Enlace Average')

    print("Generación de dendrogramas completada.")

