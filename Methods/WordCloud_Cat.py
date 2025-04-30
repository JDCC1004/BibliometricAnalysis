import os
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import defaultdict
import numpy as np
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
    frecuencias = {palabra.strip(): int(freq) for palabra, freq in matches}
    palabras_clave = [palabra for palabra, freq in frecuencias.items() if freq > 1]

    co_matrix = defaultdict(lambda: defaultdict(int))
    for i, p1 in enumerate(palabras_clave):
        for p2 in palabras_clave[i + 1:]:
            co_matrix[p1][p2] += 1
            co_matrix[p2][p1] += 1

    if not co_matrix:
        continue

    df = pd.DataFrame.from_dict(co_matrix, orient='index').fillna(0).astype(int)

    G = nx.Graph()
    for p1 in df.index:
        for p2 in df.columns:
            w = df.loc[p1, p2]
            if w > 0:
                G.add_edge(p1, p2, weight=w)

    if G.number_of_edges() == 0:
        continue

    # Obtener frecuencia para cada nodo
    node_freq = {node: frecuencias.get(node, 1) for node in G.nodes()}
    max_freq = max(node_freq.values())
    min_freq = min(node_freq.values())

    # Asignar colores según frecuencia (más oscuro a más claro, o viceversa)
    norm = plt.Normalize(vmin=min_freq, vmax=max_freq)
    cmap = plt.colormaps.get_cmap("plasma")
    node_colors = [cmap(norm(node_freq[n])) for n in G.nodes()]

    # Tamaño proporcional al grado
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[n] * 100 for n in G.nodes()]
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    max_weight = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + (w / max_weight) * 4 for w in edge_weights]

    pos = nx.spring_layout(G, k=1.2, seed=42)

    fig, ax = plt.subplots(figsize=(14, 12))
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, node_color=node_colors, alpha=0.9)
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color='black')

    ax.set_title(f"Red de Co-ocurrencia (color por frecuencia): {archivo.replace('.txt', '')}", fontsize=15)
    ax.axis("off")
    plt.tight_layout()

    ruta_salida = os.path.join(carpeta_salida, f"co_word_{archivo.replace('.txt', '')}.png")
    plt.savefig(ruta_salida, format="png", dpi=300)
    plt.close()
    print(f"✅ Gráfico generado: {archivo}")
