from fastapi import FastAPI
from app.routers import order, wallet
from app.database import engine, Base
from app.models import order_model, wallet_model
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

# CORS 설정 시작
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 8001번 포트의 접속을 허용
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PATCH 등 모든 요청 허용
    allow_headers=["*"],         # 모든 헤더 정보 허용
)

app.include_router(order.router, prefix="/api", tags=["Order"])
app.include_router(wallet.router, prefix="/api/wallets", tags=["Wallet"])

@app.get("/")
def read_root():
    return {"message": "Order Service is running"}