
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class LibroCategoria(SQLModel, table=True):
    __tablename__ = "libro_categoria"
    lcat_id: Optional[int] = Field(default=None, primary_key=True)
    lcat_idlibro: Optional[int] = Field(default=None, foreign_key="libro.lib_id")
    lcat_idcategoria: Optional[int] = Field(default=None, foreign_key="categoria.cat_id")

    Categroria: Optional["Categoria"] = Relationship(back_populates="LibroCategoria")
    Libro: Optional["Libro"] = Relationship(back_populates="LibroCategoria")