from fastapi import Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import selectinload
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.models.usuario.modelo_usuario import Usuario
import os
from dotenv import load_dotenv
from typing import Dict, Optional, Union

load_dotenv()

# Constantes de configuración
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="autenticacion/ingresar")

def crear_token(usu_nombre: str, usu_id: int, rol_nombre: str, expires_delta: timedelta, token_type: str = "access") -> str:
    data = {
        "sub": usu_nombre,
        "id": usu_id,
        "role": rol_nombre,
        "type": token_type,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def crear_tokens(usu_nombre: str, usu_id: int, rol_nombre: str) -> Dict[str, str]:
    access_token = crear_token(
        usu_nombre, 
        usu_id, 
        rol_nombre, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
        'access'
    )
    refresh_token = crear_token(
        usu_nombre, 
        usu_id, 
        rol_nombre, 
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), 
        'refresh'
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def generar_token_activacion(usu_id: int) -> str:
    return jwt.encode(
        {
            "sub": str(usu_id),  # <- Cambio aquí
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def generar_token_recuperacion(usu_id: int) -> str:
    return jwt.encode(
        {
            "sub": str(usu_id),
            "tipo": "recuperacion",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verificar_password(clave_plana: str, clave_hash: str) -> bool:
    return bcrypt_context.verify(clave_plana, clave_hash)

def hash_password(clave: str) -> str:
    return bcrypt_context.hash(clave)

def refrescar_token(refresh_token: str) -> Dict[str, str]:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token no válido para refrescar"
            )
        return crear_tokens(payload["sub"], payload["id"], payload["role"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Refresh token inválido o expirado"
        )

def usuario_autenticado(usu_nombre: str, usu_clave: str, db) -> Optional[Usuario]:
    statement = select(Usuario).options(selectinload(Usuario.rol)).where(Usuario.usu_nombre == usu_nombre)
    usuario = db.exec(statement).first()

    if not usuario or not verificar_password(usu_clave, usuario.usu_clave):
        return None
    return usuario

async def obtener_usuario(token: str = Depends(oauth2_bearer)) -> Dict[str, Union[str, int]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token no válido para acceso"
            )
        return {
            "usu_nombre": payload["sub"],
            "usu_id": payload["id"],
            "usu_rol": payload["role"]
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

def verificar_rol(roles_permitidos: list[str]):
    async def verificar_rol_auth(usuario: dict = Depends(obtener_usuario)):
        if usuario["usu_rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para esta acción"
            )
        return usuario
    return verificar_rol_auth
