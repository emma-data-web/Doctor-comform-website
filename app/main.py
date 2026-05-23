from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import payments, webhook, book_order 


app = FastAPI(title="Brunch and Pray")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments.router, prefix="/tickets")  
app.include_router(book_order.router, prefix="/books")     
app.include_router(webhook.router)
