from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.servicio_libro import LibroService
from app.models.libro.modelo_libro import LibroCreate
from app.database.database import get_session

router = APIRouter(prefix="/libro", tags=["Libro"])


@router.post("/")
async def crear_libro(data: LibroCreate, session: Session = Depends(get_session), file: UploadFile = File(...)):
    libro = LibroService(session).crear_libro(file, data)
    if not libro:
        raise HTTPException(status_code=400, detail="Error al crear el libro")

    return libro