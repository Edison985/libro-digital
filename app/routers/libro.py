# routers/libros.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from app.services.servicio_libro import guardar_pdf

router = APIRouter()

@router.post("/subir-pdf/")
async def subir_pdf(file: UploadFile = File(...)):
    resultado = guardar_pdf(file)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@router.get("/formulario", response_class=HTMLResponse)
def formulario():
    return """
    <html>
        <body>
            <h2>Subir archivo PDF</h2>
            <form action="/subir-pdf/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="application/pdf">
                <input type="submit" value="Subir PDF">
            </form>
        </body>
    </html>
    """
