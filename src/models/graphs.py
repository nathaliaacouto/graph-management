from sqlalchemy import Column, Integer, JSON, Boolean

from ..db.database import Base

class Graph(Base):
    __tablename__ = "graphs"

    id: int = Column(Integer, primary_key=True, index=True)
    graph: str = Column(JSON, nullable=True)
    directed: bool = Column(Boolean, nullable=False, default=False)