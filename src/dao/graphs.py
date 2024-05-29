from sqlalchemy.orm import Session

from ..models.graphs import Graph


class GraphRepository:
    @staticmethod
    def find_all(db: Session) -> list[Graph]:
        return db.query(Graph).all()

    @staticmethod
    def save(db: Session, graph: Graph) -> Graph:
        if graph.id:
            db.merge(graph)
        else:
            db.add(graph)
        db.commit()
        return graph

    @staticmethod
    def find_by_id(db: Session, id: int) -> Graph:
        return db.query(Graph).filter(Graph.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Graph).filter(Graph.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        graph = db.query(Graph).filter(Graph.id == id).first()
        if graph is not None:
            db.delete(graph)
            db.commit()
