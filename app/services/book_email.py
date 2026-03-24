from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.email import conf
from app.schemas.book_schema import BookPurchaseRequest


async def send_physical_book_email(
    buyer_name: str,
    buyer_email: str,
    buyer_address: str,
    book_title: str,
    quantity: int
):

    body = f"""
    <h2>Thank you for your order!</h2>

    <p>Hello {buyer_name},</p>

    <p>Your order has been received successfully.</p>

    <b>Order Details:</b>

    <ul>
        <li>Book: {book_title}</li>
        <li>Quantity: {quantity}</li>
        <li>Shipping Address: {buyer_address}</li>
    </ul>

    <p>Your book will be shipped soon.</p>

    <p>Thank you for your support </p>
    """

    message = MessageSchema(
        subject="Your Book Order Confirmation",
        recipients=[buyer_email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(message)




async def send_physical_book_owner_email(book_request: BookPurchaseRequest, owner_email: str):
   
    body = f"""
    <h2>New Book Order Received!</h2>

    <p>Buyer Details:</p>
    <ul>
        <li>Name: {book_request.buyer_name}</li>
        <li>Email: {book_request.buyer_email}</li>
        <li>Phone: {book_request.buyer_phone or 'Not provided'}</li>
        <li>Shipping Address: {book_request.buyer_address}</li>
    </ul>

    <p>Order Details:</p>
    <ul>
        <li>Book: {book_request.book_title}</li>
        <li>Quantity: {book_request.quantity}</li>
    </ul>

    <p>Please prepare this order for shipment.</p>
    """

    message = MessageSchema(
        subject="New Book Order Notification",
        recipients=[owner_email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)