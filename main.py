from fastapi import FastAPI, Form, File, UploadFile
from typing import Annotated
import asyncio
from src import functions

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
