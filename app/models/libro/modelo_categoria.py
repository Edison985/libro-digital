from sqlmodel import SQLModel, Field
from typing import Optional

class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"
    cat_id: Optional[int] = Field(default=None, primary_key=True)
    cat_nombre: str = Field(max_length=50, unique=True)
    cat_descripcion: Optional[str]

class CategoriaCreate(SQLModel):
    cat_nombre: str
    cat_descripcion: Optional[str] = None

    class Config:
        orm_mode = True

class CategoriaUpdate(SQLModel):
    cat_nombre: Optional[str] = None
    cat_descripcion: Optional[str] = None

    class Config:
        orm_mode = True

class CategoriaResponse(SQLModel):
    cat_id: int
    cat_nombre: str
    cat_descripcion: Optional[str] = None

    class Config:
        orm_mode = True
