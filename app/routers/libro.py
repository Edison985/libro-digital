from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.servicio_libro import LibroService
from app.models.libro.modelo_libro import LibroCreate
from app.database.database import get_session

router = APIRouter(prefix="/libro", tags=["Libro"])

from fastapi import Form


class LibroCreateForm:
    def __init__(
        self,
        lib_titulo: str = Form(...),
        lib_descripcion: str = Form(...),
        lib_fecha: str = Form(...),
        lib_precio: float = Form(...),
        lib_url: str = Form(...),
        lib_ideditorial: int = Form(...),
        lib_estado: bool = Form(...)
    ):
        self.lib_titulo = lib_titulo
        self.lib_descripcion = lib_descripcion
        self.lib_fecha = lib_fecha
        self.lib_precio = lib_precio
        self.lib_url = lib_url
        self.lib_ideditorial = lib_ideditorial
        self.lib_estado = lib_estado

@router.post("/")
async def crear_libro(
    data: LibroCreateForm = Depends(),  # ✅ usa tu clase como dependencia
    session: Session = Depends(get_session),
    file: UploadFile = File(...)
):
    # Convertimos a LibroCreate (pydantic) si es necesario
    libro_data = LibroCreate(**data.__dict__)
    
    libro = LibroService(session).crear_libro(file, libro_data)
    if not libro:
        raise HTTPException(status_code=400, detail="Error al crear el libro")

    return libro
