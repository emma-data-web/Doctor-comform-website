from fastapi_mail import FastMail, MessageSchema, MessageType
import base64
from app.core.email import conf
import os 
import uuid

async def send_ticket_email(to_email: str, qr_base64: str):
    # Convert base64 to bytes
    qr_bytes = base64.b64decode(qr_base64)

    # Save QR to a temporary file
    file_path = f"ticket_{uuid.uuid4()}.png"
    with open(file_path, "wb") as f:
        f.write(qr_bytes)

    message = MessageSchema(
        subject="Your Ticket Is Ready!",
        recipients=[to_email],
        body="""
        <p>Here is your ticket. Scan the QR code at the event.</p>
        """,
        subtype=MessageType.html,
        attachments=[file_path]  #  pass file path
    )

    fm = FastMail(conf)
    try: 
        await fm.send_message(message)
    finally:
        if os.path.exists(file_path):
         os.remove(file_path)

    # Optional: delete file after sending
    os.remove(file_path)