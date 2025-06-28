# services/servicio_libros.py
import os
import shutil
from app.models.libro.modelo_libro import Libro, LibroCreate

CARPETA_LIBROS = "/root/libros"
os.makedirs(CARPETA_LIBROS, exist_ok=True)


class LibroService:
    def __init__(self, session):
        self.session = session

  

    def crear_libro(self, file, data: LibroCreate) -> Libro:
        if not file.filename.lower().endswith(".pdf"):
            return {"error": "Solo se permiten archivos PDF"}

        ruta_destino = os.path.join(CARPETA_LIBROS, file.filename)

        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        libro = Libro.from_orm(data)
        libro.lib_url = file.filename
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)

        return libro
