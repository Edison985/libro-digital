import mercadopago

sdk = mercadopago.SDK("")
print("Iniciando prueba de Mercado Pago...")  # ← Esto debe verse sí o sí

request = {
    "items": [
        {
            "title": "Libro de prueba",
            "description": "Versión digital",
            "quantity": 1,
            "currency_id": "COP",
            "unit_price": 1000.0,
        }
    ],
    "payer": {
        "email": "test_user_63274575@testuser.com"
    },
    "back_urls": {
        "success": "https://www.tusitio.com/success",
        "failure": "https://www.tusitio.com/failure",
        "pending": "https://www.tusitio.com/pending"
    },
    "auto_return": "approved",
}

try:
    preference_response = sdk.preference().create(request)
    preference = preference_response["response"]
    print("Sandbox Init Point:", preference.get("sandbox_init_point"))
    print("Link Real:", preference.get("init_point"))  # solo si quisieras verlo
except Exception as e:
    print("Ocurrió un error:", e)
