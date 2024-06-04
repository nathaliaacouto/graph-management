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


async def read_graph_csv_by_file(file, directed=False):
    # Leitura do conteúdo do arquivo CSV enviado
    content = await file.read()
    # Decodificação do conteúdo para string
    csv_str = content.decode("utf-8")

    # Utilizando pandas para ler o CSV a partir da string
    df = pd.read_csv(StringIO(csv_str))

    first_three_columns = df.columns[:3]
    source_column = first_three_columns[0]
    target_column = first_three_columns[1]
    weight_column = first_three_columns[2] if len(
        first_three_columns) == 3 else None

    if weight_column is not None:
        # trocar nome da coluna para 'weight'
        df.rename(columns={weight_column: 'weight'}, inplace=True)
        weight_column = 'weight'

    if directed:
        # Criação do grafo utilizando NetworkX
        G = nx.from_pandas_edgelist(
            df, source=source_column, target=target_column, edge_attr=weight_column, create_using=nx.DiGraph)
    else:
        # Criação do grafo utilizando NetworkX
        G = nx.from_pandas_edgelist(
            df, source=source_column, target=target_column, edge_attr=weight_column)
    return G, convert_graph_to_json(G)


async def read_graph_csv_by_string(csv_str, directed=False):
    """
    Read graph from csv string
    """
    # Utilizando pandas para ler o CSV a partir da string
    df = pd.read_csv(StringIO(csv_str))

    first_three_columns = df.columns[:3]
    source_column = first_three_columns[0]
    target_column = first_three_columns[1]
    weight_column = first_three_columns[2] if len(
        first_three_columns) == 3 else None

    if weight_column is not None:
        # trocar nome da coluna para 'weight'
        df.rename(columns={weight_column: 'weight'}, inplace=True)
        weight_column = 'weight'

    if directed:
        # Criação do grafo utilizando NetworkX
        G = nx.from_pandas_edgelist(
            df, source=source_column, target=target_column, edge_attr=weight_column, create_using=nx.DiGraph)
    else:
        # Criação do grafo utilizando NetworkX
        G = nx.from_pandas_edgelist(
            df, source=source_column, target=target_column, edge_attr=weight_column)
    return G, convert_graph_to_json(G)


def exists_edge(graph, source, target):
    """
    Check if an edge exists in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - source: The source node.
    - target: The target node.

    Returns:
    - exists: True if the edge exists, False otherwise.
    """
    return graph.has_edge(source, target)


def exists_node(graph, node):
    """
    Check if a node exists in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to be checked.

    Returns:
    - exists: True if the node exists, False otherwise.
    """
    return graph.has_node(node)


def get_incoming_edges(graph, node):
    """
    Get the incoming edges of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the incoming edges.

    Returns:
    - edges: The incoming edges of the node.
    """
    return list(graph.in_edges(node, data=True))


def get_outgoing_edges(graph, node):
    """
    Get the outgoing edges of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the outgoing edges.

    Returns:
    - edges: The outgoing edges of the node.
    """
    return list(graph.out_edges(node, data=True))


def get_adjacent_edges(graph, node, directed=False):
    """
    Get the adjacent edges of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the adjacent edges.

    Returns:
    - edges: The adjacent edges of the node.
    """
    if not directed:
        return list(graph.edges(node, data=True))

    incoming_edges = get_incoming_edges(graph, node)
    outgoing_edges = get_outgoing_edges(graph, node)

    return {
        "incoming": incoming_edges,
        "outgoing": outgoing_edges
    }


def get_adjacent_degree(graph, node, directed=False):
    """
    Get the adjacent degree of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the adjacent degree.

    Returns:
    - degree: The adjacent degree of the node.
    """
    if not directed:
        return graph.degree(node)

    incoming_degree = len(get_incoming_edges(graph, node))
    outgoing_degree = len(get_outgoing_edges(graph, node))

    return {
        "incoming": incoming_degree,
        "outgoing": outgoing_degree
    }


def get_has_edge(graph, source, target):
    """
    Get the weight of an edge in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - source: The source node.
    - target: The target node.

    Returns:
    - weight: The weight of the edge.
    """
    return graph.has_edge(source, target)


def get_shortest_path(graph, source, target):
    """
    Get the shortest path between two nodes in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - source: The source node.
    - target: The target node.

    Returns:
    - path: The shortest path between the nodes.
    """
    result = {
        "path": None,
        "shortest_path_length": None,
        "message": "No path found!"
    }
    try:
        result['path'] = nx.shortest_path(
            graph, source, target, weight='weight')
        result['shortest_path_length'] = nx.shortest_path_length(
            graph, source=source, target=target, weight='weight')
        result['message'] = "Shortest path found successfully!"
    except nx.exception.NetworkXNoPath as e:
        result['message'] = "No path found! Error: " + str(e)
    return result


def get_eccentricity_node(graph, node):
    """
    Get the eccentricity of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the eccentricity.

    Returns:
    - eccentricity: The eccentricity of the node.
    """
    try:
        result = nx.eccentricity(graph, v=node)
    except nx.exception.NetworkXError as e:
        result = "Error in Graph: " + str(e)

    return result


def is_eulerian(graph):
    """
    Check if a graph is Eulerian.

    Parameters:
    - graph: The NetworkX graph.

    Returns:
    - is_eulerian: True if the graph is Eulerian, False otherwise.
    """
    return nx.is_eulerian(graph)


def is_semi_eulerian(graph):
    """
    Check if a graph is semi-Eulerian.

    Parameters:
    - graph: The NetworkX graph.

    Returns:
    - is_semi_eulerian: True if the graph is semi-Eulerian, False otherwise.
    """
    return nx.is_semieulerian(graph)


def get_radius(graph):
    """
    Get the radius of a graph.

    Parameters:
    - graph: The NetworkX graph.

    Returns:
    - radius: The radius of the graph.
    """
    try:
        result = nx.radius(graph)
    except nx.exception.NetworkXError as e:
        result = "Error in Graph: " + str(e)

    return result


def get_diameter(graph):
    """
    Get the diameter of a graph.

    Parameters:
    - graph: The NetworkX graph.

    Returns:
    - diameter: The diameter of the graph.
    """
    try:
        result = nx.diameter(graph)
    except nx.exception.NetworkXError as e:
        result = "Error in Graph: " + str(e)

    return result

def get_pendent_node(graph, node):
    """
    Get the pendent nodes of a node in a graph.

    Parameters:
    - graph: The NetworkX graph.
    - node: The node to get the pendent nodes.

    Returns:
    - pendent_nodes: The pendent nodes of the node.
    """
    if(graph.degree(node) == 1):
        return True
    else:
        return False


def generate_image_from_graph(graph, directed, filename='graph.png'):
    """
    Generate and save a PNG image from a graph, and return the absolute path of the saved image.

    Parameters:
    - graph: The NetworkX graph to be drawn.
    - filename: The name of the file where the image will be saved (default is 'graph.png').

    Returns:
    - abs_path: The absolute path of the saved image file.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    if directed:
        options = {
            'width': 3,
            'arrowstyle': '-|>',
            'arrowsize': 25,
            'arrows': True,
        }
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos, edge_color='gray',
                               **options)
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))
    else:
        options = {
            'width': 3,
        }
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos, edge_color='gray',
                               **options)
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))

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
