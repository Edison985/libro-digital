
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class LibroAutor(SQLModel, table=True):
    __tablename__ = "libro_autor"
    laut_id: Optional[int] = Field(default=None, primary_key=True)
    laut_idlibro: Optional[int] = Field(default=None, foreign_key="libro.lib_id")
    laut_idautor: Optional[int] = Field(default=None, foreign_key="autor.aut_id")

    autor: Optional["Autor"] = Relationship(back_populates="libro_autor")
    libro: Optional["Libro"] = Relationship(back_populates="libro_autor")