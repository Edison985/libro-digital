# app/services/servicio_pago.py
import mercadopago
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

sdk = mercadopago.SDK(ACCESS_TOKEN)

def crear_preferencia_pago(nombre_producto: str, precio: float, cantidad: int = 1) -> str:
    preference_data = {
        "items": [
            {
                "title": nombre_producto,
                "quantity": cantidad,
                "currency_id": "COP",
                "unit_price": precio
            }
        ],
        # "payer": {
        #     "email": "test_user_63274575@testuser.com"  # Solo para pruebas
        # },
        "back_urls": {
            "success": "https://www.tusitio.com/success",
            "failure": "https://www.tusitio.com/failure",
            "pending": "https://www.tusitio.com/pending"
        },
        "auto_return": "approved"
    }

    try:
        response = sdk.preference().create(preference_data)
        #return response["response"]["sandbox_init_point"]  # devuelves solo sandbox
        return response["response"]["init_point"]
    except Exception as e:
        raise Exception(f"Error creando preferencia: {e}")
