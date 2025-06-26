# services/servicio_libros.py
import os
import shutil

CARPETA_LIBROS = "/root/libros"
os.makedirs(CARPETA_LIBROS, exist_ok=True)

def guardar_pdf(file):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Solo se permiten archivos PDF"}

    ruta_destino = os.path.join(CARPETA_LIBROS, file.filename)

    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"mensaje": f"Archivo '{file.filename}' subido correctamente"}
