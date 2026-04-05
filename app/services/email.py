from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.email import conf
import base64
import tempfile
import os


async def send_ticket_email(to_email: str, qr_base64: str):
    
    html_content = """
    <h2>Welcome to Brunch & Pray! 🎉</h2>
    <p>Your ticket is confirmed. Please find your QR code attached.</p>
    <p>Present it at the event entrance to get in.</p>
    <p>See you there! </p>
    """

    # Save QR to temp file
    qr_bytes = base64.b64decode(qr_base64)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.write(qr_bytes)
    tmp.close()

    message = MessageSchema(
        subject="Your Ticket Is Ready!",
        recipients=[to_email],
        body=html_content,
        subtype=MessageType.html,
        attachments=[tmp.name]
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    # Clean up temp file
    os.unlink(tmp.name)