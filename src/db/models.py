from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing integer ID
    task = Column(String, index=True)
    completed = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
