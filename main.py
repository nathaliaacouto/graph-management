from fastapi import FastAPI, Form, File, UploadFile, Depends
from typing import Annotated
from src import functions
from src.db.database import engine, Base, get_db
from src.models.graphs import Graph
from src.dao.graphs import GraphRepository
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create-graph/")
async def create_graph_api(csv_str: Annotated[str, Form(...)] = None, file: UploadFile = File(None), directed: Annotated[bool, Form(...)] = False, db: Session = Depends(get_db)):
    graphs = None
    if csv_str:
        _, graphs = await functions.read_graph_csv_by_string(csv_str, directed=directed)
    if file:
        _, graphs = await functions.read_graph_csv_by_file(file, directed=directed)
    if graphs is not None:
        graph_object = GraphRepository.save(
            db, Graph(graph=graphs, directed=directed))
        return {"message": "Graph created successfully!", "id": graph_object.id}
    return {"message": "Graph not created!"}


@app.get("/get-graph/")
def get_graph_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        return {"message": "Graph found successfully!", "graph": graph.graph}
    return {"message": "Graph not found!"}


@app.put("/add-edge/")
def add_edge_api(id: int, source: str = Form(...), target: str = Form(...), weight: Annotated[int, Form(...)] = None, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        # graph.graph.add_edge(source, target)
        graph_object = functions.convert_json_to_graph(graph.graph)
        if weight:
            graph_object.add_edge(source, target, weight=weight)
        else:
            graph_object.add_edge(source, target)

        json_graph = functions.convert_graph_to_json(graph_object)
        graph.graph = json_graph
        GraphRepository.save(db, graph)
        return {"message": "Edge added successfully!"}
    return {"message": "Graph not found!"}


@app.put("/add-node/")
def add_node_api(id: int, node: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        graph_object.add_node(node)

        json_graph = functions.convert_graph_to_json(graph_object)
        graph.graph = json_graph
        GraphRepository.save(db, graph)
        return {"message": "Node added successfully!"}
    return {"message": "Graph not found!"}


@app.get("/get-order/")
def get_order_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Order retrieved successfully!", "order": graph_object.order()}
    return {"message": "Graph not found!"}


@app.get("/get-degree/")
def get_degree_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Degree retrieved successfully!", "degree": dict(graph_object.degree)}
    return {"message": "Graph not found!"}


@app.get("/get-adjacent-edges/")
def get_adjacent_edges_api(id: int, node: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        if functions.exists_node(graph_object, node):
            return {"message": "Adjacent edges retrieved successfully!", "edges": functions.get_adjacent_edges(graph_object, node, directed=graph.directed)}
        return {"message": "Node not found!"}
    return {"message": "Graph not found!"}


@app.get("/get-adjacent-degree/")
def get_adjacent_degree_api(id: int, node: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        if functions.exists_node(graph_object, node):
            return {"message": "Adjacent edges with degree retrieved successfully!", "edges": functions.get_adjacent_degree(graph_object, node, directed=graph.directed)}
        return {"message": "Node not found!"}
    return {"message": "Graph not found!"}


@app.get("/get-has-edge/")
def get_has_edge_api(id: int, source: str = Form(...), target: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        if functions.exists_node(graph_object, source) and functions.exists_node(graph_object, target):
            return {"message": "Edge found successfully!", "exists": functions.get_has_edge(graph_object, source, target)}
        return {"message": "Some node not found!"}
    return {"message": "Graph not found!"}


@app.get("/get-shortest-path/")
def get_shortest_path_api(id: int, source: str = Form(...), target: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        if functions.exists_node(graph_object, source) and functions.exists_node(graph_object, target):
            return {"result": functions.get_shortest_path(graph_object, source, target)}
        return {"message": "Some node not found!"}
    return {"message": "Graph not found!"}


@app.get("/get-eccentricity-node/")
def get_eccentricity_node_api(id: int, node: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        if functions.exists_node(graph_object, node):
            return {"message": "Eccentricity node retrieved successfully!", "eccentricity": functions.get_eccentricity_node(graph_object, node)}
        return {"message": "Node not found!"}
    return {"message": "Graph not found!"}


@app.get("/is-eulerian/")
def is_eulerian_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Eulerian graph retrieved successfully!", "is_eulerian": functions.is_eulerian(graph_object)}
    return {"message": "Graph not found!"}


@app.get("/is-semi-eulerian/")
def is_semi_eulerian_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Semi-Eulerian graph retrieved successfully!", "is_semi_eulerian": functions.is_semi_eulerian(graph_object)}
    return {"message": "Graph not found!"}


@app.get("/adjacency-matrix/")
def adjacency_matrix_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        matrix = functions.generate_adjacency_matrix(graph_object)
        return {"message": "Adjacency matrix generated successfully!", "result": matrix}
    return {"message": "Graph not found!"}


@app.get("/get-radius/")
def get_radius_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Radius retrieved successfully!", "radius": functions.get_radius(graph_object)}
    return {"message": "Graph not found!"}


@app.get("/get-diameter/")
def get_diameter_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        return {"message": "Diameter retrieved successfully!", "diameter": functions.get_diameter(graph_object)}
    return {"message": "Graph not found!"}


@app.get("/get-image-graph/")
def get_image_graph_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        directed = graph.directed
        image_path = functions.generate_image_from_graph(
            graph_object, directed, 'graph.png')
        return {"message": "Image generated successfully!", "image": image_path}
    return {"message": "Graph not found!"}


@app.post("/read-graph-csv-by-file/")
async def read_graph_csv_by_file_api(file: UploadFile = File()):
    try:
        graphs = await functions.read_graph_csv_by_file(file)
        image_path = functions.generate_image_from_graph(graphs, 'graph.png')
        response = {
            "file_path": file.filename,
            "message": "Graph read successfully!",
            "order": graphs.order(),
            "size": graphs.size(),
            "nodes": list(graphs.nodes),
            "edges": list(graphs.edges),
            "degree": dict(graphs.degree),
            "image": image_path
        }
    except Exception as e:
        response = {
            "file_path": file.filename,
            "message": str(e)
        }
    return response


@app.post("/read-graph-string")
async def read_graph_csv_by_string_api(csv_str: Annotated[str, Form(...)]):
    try:
        graphs = await functions.read_graph_csv_by_string(csv_str)
        image_path = functions.generate_image_from_graph(graphs, 'graph.png')
        response = {
            "message": "Graph read successfully!",
            "order": graphs.order(),
            "size": graphs.size(),
            "nodes": list(graphs.nodes),
            "edges": list(graphs.edges),
            "degree": dict(graphs.degree),
            "image": image_path
        }
    except Exception as e:
        response = {
            "message": str(e)
        }
    return response
