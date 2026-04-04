from fastapi import FastAPI
from app.routers import order
from app.database import engine, Base
from app.models import order_model, user_model
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service",
    docs_url="/api/orders/docs",
    openapi_url="/api/orders/openapi.json",
    redirect_slashes=False
)

origins = ["https://woowabeavers.cloud", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Order Service is running"}
