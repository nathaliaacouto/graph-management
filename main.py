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
async def create_graph_api(csv_str: Annotated[str, Form(...)] = None, file: UploadFile = File(None), db: Session = Depends(get_db)):
    graphs = None
    if csv_str:
        _, graphs = await functions.read_graph_csv_by_string(csv_str)
    if file:
        _, graphs = await functions.read_graph_csv_by_file(file)
    if graphs is not None:
        graph_object = GraphRepository.save(db, Graph(graph=graphs))
        return {"message": "Graph created successfully!", "id": graph_object.id}
    return {"message": "Graph not created!"}


@app.get("/get-graph/")
def get_graph_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        return {"message": "Graph found successfully!", "graph": graph.graph}
    return {"message": "Graph not found!"}


@app.put("/add-edge/")
def add_edge_api(id: int, source: str = Form(...), target: str = Form(...), db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        # graph.graph.add_edge(source, target)
        graph_object = functions.convert_json_to_graph(graph.graph)
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

@app.get("/adjacency-matrix/")
def adjacency_matrix_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        matrix = functions.generate_adjacency_matrix(graph_object)
        return {"message": "Adjacency matrix generated successfully!", "result": matrix}
    return {"message": "Graph not found!"}

@app.get("/get-image-graph/")
def get_image_graph_api(id: int, db: Session = Depends(get_db)):
    graph = GraphRepository.find_by_id(db, id)
    if graph is not None:
        graph_object = functions.convert_json_to_graph(graph.graph)
        image_path = functions.generate_image_from_graph(
            graph_object, 'graph.png')
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
