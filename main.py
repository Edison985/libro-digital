# main.py

from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database.database import engine
from app.models.usuario.modelo_usuario import Usuario
from app.models.usuario.modelo_rol import Rol
from app.models.libro.modelo_libro import Libro, LibroCreate
from app.models.libro.modelo_editorial import Editorial
from app.models.libro.modelo_autor import Autor
from app.models.libro.modelo_categoria import Categoria
from app.models.libro.modelo_librocategoria import LibroCategoria
from app.models.libro.modelo_libroautor import LibroAutor



from app.routers import usuario, autenticacion, pago, autor, categoria, editorial, libro


app = FastAPI(
    title="Sistema Mixera",
   
)


def crear_tablas():
    SQLModel.metadata.create_all(engine)

crear_tablas()

app.include_router(usuario.router)
app.include_router(autenticacion.router)
app.include_router(pago.router)
app.include_router(autor.router)
app.include_router(categoria.router)
app.include_router(editorial.router)
app.include_router(libro.router)