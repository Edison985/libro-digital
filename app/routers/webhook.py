# app/routers/webhook.py
from fastapi import APIRouter, Request
import hmac
import hashlib
import os

router = APIRouter()

@router.post("/webhook")
async def recibir_webhook(request: Request):
    body = await request.body()
    evento = await request.json()

    # Verificar clave secreta si definiste una (opcional pero recomendado)
    signature_header = request.headers.get("X-Hub-Signature")
    clave_secreta = os.getenv("MP_WEBHOOK_SECRET")  # misma que pusiste en el panel

    if signature_header and clave_secreta:
        sha_name, signature = signature_header.split('=')
        mac = hmac.new(clave_secreta.encode(), msg=body, digestmod=hashlib.sha256)
        if not hmac.compare_digest(mac.hexdigest(), signature):
            return {"error": "Firma inválida"}, 400

    print("📥 Webhook recibido:", evento)
    return {"status": "ok"}
