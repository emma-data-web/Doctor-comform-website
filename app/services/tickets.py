import qrcode
import io
import base64
from app.db.tickets import create_ticket
import uuid

def generate_ticket_qr(ticket_id: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"https://doctor-comform-website.onrender.com/welcome/{ticket_id}")
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # Convert to base64 to save in DB or email
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    return qr_base64

def create_ticket_with_qr(db, buyer_email: str, payment_id: str):
    # 1 Generate unique ticket ID
    ticket_id = str(uuid.uuid4())

    # 2 Generate QR code
    qr_code = generate_ticket_qr(ticket_id)

    # Save ticket in DB
    ticket = create_ticket(db, buyer_email, payment_id, qr_code)
    return ticket