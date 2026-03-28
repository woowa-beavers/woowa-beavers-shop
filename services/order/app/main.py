from fastapi import FastAPI
from app.routers import order
from app.database import engine, Base
from app.models import order_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

app.include_router(order.router, prefix="/api", tags=["Order"])

@app.get("/")
def read_root():
    return {"message": "Order Service is running"}