from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.database.database import get_session
from app.models.libro.modelo_editorial import Editorial, EditorialCreate, EditorialUpdate
from app.services.servicio_editorial import EditorialService

router = APIRouter(prefix="/editorial", tags=["Editorial"])


@router.get("/", response_model=List[Editorial])
def listar(session: Session = Depends(get_session)):
    return EditorialService(session).listar_editoriales()

@router.post("/", response_model=Editorial, status_code=201)
def crear(data: EditorialCreate, session: Session = Depends(get_session)):
    return EditorialService(session).crear_editorial(data)

@router.put("/{edi_id}", response_model=Editorial)
def actualizar(edi_id: int, data: EditorialUpdate, session: Session = Depends(get_session)):
    return EditorialService(session).actualizar_editorial(edi_id, data)
