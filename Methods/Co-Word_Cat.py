import os
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from collections import defaultdict
import community  # from python-louvain

carpeta_tablas = "../Tables"
carpeta_salida = "../Graphics/Co-Word/Cat"

os.makedirs(carpeta_salida, exist_ok=True)

for archivo in os.listdir(carpeta_tablas):
    if not archivo.endswith(".txt"):
        continue

    ruta = os.path.join(carpeta_tablas, archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read()

    matches = re.findall(r"│ ([^│]+?)\s+│\s+(\d+)\s+│", texto)
    palabras_frecuencias = {palabra.strip(): int(frecuencia) for palabra, frecuencia in matches}
    palabras_clave = [palabra for palabra, frecuencia in palabras_frecuencias.items() if frecuencia > 1]

    # Construcción de matriz de co-ocurrencia
    co_matrix = defaultdict(lambda: defaultdict(int))
    for i, palabra1 in enumerate(palabras_clave):
        for palabra2 in palabras_clave[i + 1:]:
            co_matrix[palabra1][palabra2] += 1
            co_matrix[palabra2][palabra1] += 1

    if not co_matrix:
        continue  # Saltar si no hay co-ocurrencias

    df = pd.DataFrame.from_dict(co_matrix, orient='index').fillna(0).astype(int)

    G = nx.Graph()
    for p1 in df.index:
        for p2 in df.columns:
            w = df.loc[p1, p2]
            if w > 0:
                G.add_edge(p1, p2, weight=w)

    if G.number_of_edges() == 0:
        continue

    degrees = dict(G.degree())
    node_sizes = [300 + degrees[n] * 80 for n in G.nodes()]
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + (w / max_weight) * 4 for w in edge_weights]

    # Detección de comunidades
    partition = community.best_partition(G)
    num_communities = len(set(partition.values()))
    cmap = plt.colormaps.get_cmap('tab10')
    colors = [cmap(i % 10) for i in partition.values()]

    pos = nx.spring_layout(G, k=1.2, seed=42)

    fig, ax = plt.subplots(figsize=(14, 12))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, node_color=colors, alpha=0.9)
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color='black')

    ax.set_title(f"Red de Co-ocurrencia: {archivo.replace('.txt', '')}", fontsize=15)
    ax.axis("off")
    plt.tight_layout()

    nombre_salida = os.path.join(carpeta_salida, f"co_word_{archivo.replace('.txt', '')}.png")
    plt.savefig(nombre_salida, format="png", dpi=300)
    plt.close()
    print(f"✅ Gráfico generado para: {archivo}")
