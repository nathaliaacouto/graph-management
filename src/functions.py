import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO


async def read_graph_csv_by_file(file):
    # Leitura do conteúdo do arquivo CSV enviado
    content = await file.read()
    # Decodificação do conteúdo para string
    csv_str = content.decode("utf-8")

    # Utilizando pandas para ler o CSV a partir da string
    df = pd.read_csv(StringIO(csv_str))

    first_three_columns = df.columns[:3]
    source_column = first_three_columns[0]
    target_column = first_three_columns[1]

    # Criação do grafo utilizando NetworkX
    G = nx.from_pandas_edgelist(df, source=source_column, target=target_column)
    return G


async def read_graph_csv_by_string(csv_str):
    """
    Read graph from csv string
    """
    # Utilizando pandas para ler o CSV a partir da string
    df = pd.read_csv(StringIO(csv_str))

    first_three_columns = df.columns[:3]
    source_column = first_three_columns[0]
    target_column = first_three_columns[1]

    # Criação do grafo utilizando NetworkX
    G = nx.from_pandas_edgelist(df, source=source_column, target=target_column)
    return G


def generate_image_from_graph(graph, filename='graph.png'):
    """
    Generate and save a PNG image from a graph, and return the absolute path of the saved image.

    Parameters:
    - graph: The NetworkX graph to be drawn.
    - filename: The name of the file where the image will be saved (default is 'graph.png').

    Returns:
    - abs_path: The absolute path of the saved image file.
    """
    plt.figure(figsize=(12, 8))
    nx.draw_networkx(graph, with_labels=True)
    plt.savefig(filename, format='png')
    plt.close()  # Fecha a figura para liberar memória

    # Obter o caminho absoluto do arquivo salvo
    abs_path = os.path.abspath(filename)
    return abs_path
