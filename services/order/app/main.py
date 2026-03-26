from fastapi import FastAPI
from app.routers import order

app = FastAPI(title="Order Service")

app.include_router(order.router, prefix="/api", tags=["Order"])

# 서버가 잘 켜졌는지 확인
@app.get("/")
def read_root():
    return {"message": "Order Service is running"}