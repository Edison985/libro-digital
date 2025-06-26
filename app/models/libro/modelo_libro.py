
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    lib_id: Optional[int] = Field(default=None, primary_key=True)
    lib_titulo: str = Field(max_length=150)
    lib_descripcion: Optional[str]
    lib_fecha: Optional[datetime.date]
    lib_precio: Optional[int]
    lib_url: str
    lib_ideditorial: Optional[int] = Field(default=None, foreign_key="editorial.edi_id")
    lib_estado: bool