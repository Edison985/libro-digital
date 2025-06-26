from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlmodel import Session
from jose import JWTError
from pydantic import BaseModel
from app.models.usuario.modelo_usuario import UsuarioCreate
from app.services.servicio_usuario import (
    registrar_usuario,
    activar_usuario,
    actualizar_clave,
    enviar_solicitud
)
from app.database.database import get_session

router = APIRouter(prefix="/usuario", tags=["Usuario"])

class RestablecerClave(BaseModel):
    token: str
    nueva_clave: str

@router.post("/registrar", response_model=dict)
async def registrar(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    try:
        return await registrar_usuario(usuario, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/verificar", response_model=dict)
def verificar_usuario(token: str = Query(...), db: Session = Depends(get_session)):
    try:
        return activar_usuario(token, db)
    except (ValueError, JWTError):
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    except Exception:
        raise HTTPException(status_code=500, detail="Error del servidor al verificar")

@router.post("/recuperar", response_model=dict)
async def solicitar_recuperacion(usu_correo: str = Body(..., embed=True), db: Session = Depends(get_session)):
    try:
        return await enviar_solicitud(usu_correo, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al enviar el correo de recuperación")

@router.post("/restablecer", response_model=dict)
def restablecer_clave(datos: RestablecerClave, db: Session = Depends(get_session)):
    try:
        return actualizar_clave(datos.token, datos.nueva_clave, db)
    except (ValueError, JWTError):
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo restablecer la contraseña")
