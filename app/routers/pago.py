# app/routers/pago.py
from fastapi import APIRouter, Query
from app.services.servicio_pago import crear_preferencia_pago

router = APIRouter(prefix="/pago", tags=["Pago"])

@router.get("/crear", response_model=dict)
def generar_link_pago(
    nombre: str = Query("La carrera de la muerte"),
    precio: float = Query(5000.0),
    cantidad: int = Query(1)
):
    try:
        link = crear_preferencia_pago(nombre, precio, cantidad)
        return {"link_pago": link}
    except Exception as e:
        return {"error": str(e)}
