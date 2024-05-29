from sqlalchemy import Column, Integer, String, JSON

from ..db.database import Base

class Graph(Base):
    __tablename__ = "graphs"

    id: int = Column(Integer, primary_key=True, index=True)
    graph: str = Column(JSON, nullable=True)