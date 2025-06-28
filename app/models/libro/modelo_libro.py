
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date


class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    lib_id: Optional[int] = Field(default=None, primary_key=True)
    lib_titulo: str = Field(max_length=150)
    lib_descripcion: Optional[str]
    lib_fecha: date = Field(default_factory=date.today)
    lib_precio: Optional[int]
    lib_url: str
    lib_ideditorial: Optional[int] = Field(default=None, foreign_key="editorial.edi_id")
    lib_estado: bool

    Editorial: Optional["Editorial"] = Relationship(back_populates="Libro")
    LibroCategoria: Optional["LibroCategoria"] = Relationship(back_populates="Libro")
    LibroAutor: Optional["LibroAutor"] = Relationship(back_populates="Libro")
    

class LibroCreate(SQLModel):
    lib_titulo: str
    lib_descripcion: Optional[str] = None
    lib_fecha: Optional[datetime.date] = None
    lib_precio: int
    lib_url: str
    lib_ideditorial: Optional[int] = None
    lib_estado: bool

    class Config:
        orm_mode = True

class LibroUpdate(SQLModel):
    lib_titulo: Optional[str] = None
    lib_descripcion: Optional[str] = None
    lib_fecha: Optional[datetime.date] = None
    lib_precio: Optional[int] = None
    lib_url: Optional[str] = None
    lib_ideditorial: Optional[int] = None
    lib_estado: Optional[bool] = None

    class Config:
        orm_mode = True

class LibroResponse(SQLModel):
    lib_id: int
    lib_titulo: str
    lib_descripcion: Optional[str] = None
    lib_fecha: Optional[datetime.date] = None
    lib_precio: Optional[int] = None
    lib_url: str
    lib_ideditorial: Optional[int] = None
    lib_estado: bool

    class Config:
        orm_mode = True