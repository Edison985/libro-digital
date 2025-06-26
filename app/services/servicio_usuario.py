from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from app.models.usuario.modelo_usuario import Usuario, UsuarioCreate
from app.core.auth_core import generar_token_activacion
from app.services.servicio_correo import enviar_correo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def registrar_usuario(datos: UsuarioCreate, db: Session) -> Usuario:
    usuario_existente = db.exec(
        select(Usuario).where(Usuario.usu_correo == datos.usu_correo)
    ).first()

    if usuario_existente:
        raise ValueError("Ya existe un usuario con ese correo")

    usuario = Usuario(
        usu_nombre=datos.usu_nombre,
        usu_correo=datos.usu_correo,
        usu_clave=pwd_context.hash(datos.usu_clave),
        usu_verificado=False,
        usu_idrol=2
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = generar_token_activacion(usuario.usu_id)
    enlace = f"http://localhost:8000/usuario/verificar?token={token}"
    await enviar_correo(usuario.usu_correo, enlace)

    return usuario

def activar_usuario(token: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usu_id = payload.get("sub")
        if not usu_id:
            raise ValueError("Token inválido: falta el sub")
    except JWTError:
        raise ValueError("Token inválido o expirado")

    usuario = db.exec(select(Usuario).where(Usuario.usu_id == int(usu_id))).first()
    if not usuario:
        raise ValueError("Usuario no encontrado")

    if usuario.usu_verificado:
        return {"mensaje": "La cuenta ya está verificada"}

    usuario.usu_verificado = True
    db.add(usuario)
    db.commit()

    return {"mensaje": "Cuenta activada correctamente"}

async def enviar_solicitud(usu_correo: str, db: Session) -> dict:
    usuario = db.exec(select(Usuario).where(Usuario.usu_correo == usu_correo)).first()
    if not usuario:
        raise ValueError("Usuario no encontrado")

    token = jwt.encode(
        {"sub": str(usuario.usu_id), "tipo": "recuperacion"},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    enlace = f"http://localhost:8000/usuario/restablecer?token={token}"
    await enviar_correo(usuario.usu_correo, enlace, tipo="recuperacion")

    return {"mensaje": "Correo de recuperación enviado"}

def actualizar_clave(token: str, nueva_clave: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usu_id = payload.get("sub")
        tipo = payload.get("tipo")
        if not usu_id or tipo != "recuperacion":
            raise ValueError("Token inválido o no autorizado")
    except JWTError:
        raise ValueError("Token inválido o expirado")

    usuario = db.exec(select(Usuario).where(Usuario.usu_id == int(usu_id))).first()
    if not usuario:
        raise ValueError("Usuario no encontrado")

    usuario.usu_clave = pwd_context.hash(nueva_clave)
    db.add(usuario)
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}


