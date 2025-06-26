import os
import httpx

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


async def enviar_correo(destinatario: str, enlace: str, tipo: str = "activacion"):
    if tipo == "activacion":
        asunto = "Activa tu cuenta"
        mensaje = "Haz clic en el siguiente enlace para activar tu cuenta:"
        boton = "Activar cuenta"
    else:
        asunto = "Recuperación de contraseña"
        mensaje = "Haz clic en el siguiente enlace para restablecer tu contraseña:"
        boton = "Restablecer contraseña"

    html = f"""
    <html>
      <body>
        <h2>¡Hola!</h2>
        <p>{mensaje}</p>
        <p>
          <a href="{enlace}" style="background-color: #007BFF; color: white; padding: 10px 20px;
              text-decoration: none; border-radius: 5px;">
            {boton}
          </a>
        </p>
      </body>
    </html>
    """

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [destinatario],
        "subject": asunto,
        "html": html
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.resend.com/emails", headers=headers, json=payload)
        response.raise_for_status()

