# main.py

from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database.database import engine
from app.models.usuario.modelo_usuario import Usuario
from app.models.usuario.modelo_rol import Rol


from app.routers import usuario, autenticacion, pago, autor, categoria, editorial, webhook, libro

app = FastAPI()

def crear_tablas():
    SQLModel.metadata.create_all(engine)

crear_tablas() 

app.include_router(usuario.router)
app.include_router(autenticacion.router)
app.include_router(pago.router)
app.include_router(autor.router)
app.include_router(categoria.router)
app.include_router(editorial.router)
app.include_router(webhook.router)
app.include_router(libro.router)