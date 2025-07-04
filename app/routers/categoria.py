from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database.database import get_session
from app.models.libro.modelo_categoria import Categoria, CategoriaCreate, CategoriaUpdate
from app.services.servicio_categoria import CategoriaService

router = APIRouter(prefix="/categoria", tags=["Categoría"])

@router.get("/", response_model=List[Categoria])
def listar_categorias(session: Session = Depends(get_session)):
    return CategoriaService(session).listar_categorias()

@router.post("/", response_model=Categoria, status_code=201)
def crear_categoria(data: CategoriaCreate, session: Session = Depends(get_session)):
    return CategoriaService(session).crear_categoria(data)

@router.put("/{cat_id}", response_model=Categoria)
def actualizar_categoria(cat_id: int, data: CategoriaUpdate, session: Session = Depends(get_session)):
    return CategoriaService(session).actualizar_categoria(cat_id, data)
