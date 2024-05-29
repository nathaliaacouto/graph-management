import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO


def convert_graph_to_json(graph):
    """
    Convert a NetworkX graph to a JSON object.

    Parameters:
    - graph: The NetworkX graph to be converted.

    Returns:
    - json_graph: The JSON object representing the graph.
    """
    return json_graph.node_link_data(graph)


def convert_json_to_graph(json_g):
    """
    Convert a JSON object to a NetworkX graph.

    Parameters:
    - json_graph: The JSON object representing the graph.

    Returns:
    - graph: The NetworkX graph.
    """
    return json_graph.node_link_graph(json_g)


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
    if len(first_three_columns) == 3:
        edge_attr = first_three_columns[2]
    else:
        edge_attr = None

    # Criação do grafo utilizando NetworkX
    G = nx.from_pandas_edgelist(df, source=source_column, target=target_column, edge_attr=edge_attr)
    return G, convert_graph_to_json(G)


async def read_graph_csv_by_string(csv_str):
    """
    Read graph from csv string
    """
    # Utilizando pandas para ler o CSV a partir da string
    df = pd.read_csv(StringIO(csv_str))

    first_three_columns = df.columns[:3]
    source_column = first_three_columns[0]
    target_column = first_three_columns[1]
    if len(first_three_columns) == 3:
        edge_attr = first_three_columns[2]
    else:
        edge_attr = None

    # Criação do grafo utilizando NetworkX
    G = nx.from_pandas_edgelist(df, source=source_column, target=target_column, edge_attr=edge_attr)
    return G, convert_graph_to_json(G)


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

def generate_adjacency_matrix(graph):
    """
    Generate the adjacency matrix of a graph.

    Parameters:
    - graph: The NetworkX graph.

    Returns:
    - matrix: The adjacency matrix of the graph.
    """
    print(graph.nodes)
    print(nx.adjacency_matrix(graph))
    adjacency_matrix = nx.adjacency_matrix(graph).todense().tolist()
    dict_matrix = {
        "nodes": list(graph.nodes),
        "matrix": adjacency_matrix
    }
    return dict_matrix