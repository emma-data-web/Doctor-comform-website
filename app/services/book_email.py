from fastapi_mail import FastMail, MessageSchema, MessageType



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

    <p>Thank you for your support ❤️</p>
    """

    message = MessageSchema(
        subject="Your Book Order Confirmation",
        recipients=[buyer_email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(message)