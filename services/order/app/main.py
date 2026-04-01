from fastapi import FastAPI
from app.routers import order, wallet
from app.database import engine, Base
from app.models import order_model, wallet_model
from fastapi.middleware.cors import CORSMiddleware

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

# CORS 설정
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://woowabeavers.cloud"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order.router)
app.include_router(wallet.router)

# ALB Health Check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Order Service is running"}