from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    task = Column(Text)
