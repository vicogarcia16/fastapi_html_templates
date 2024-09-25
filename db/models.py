from sqlalchemy import Column, Integer, String
from db.database import Base

class Film(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    director = Column(String)