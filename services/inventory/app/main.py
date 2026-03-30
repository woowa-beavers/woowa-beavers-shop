from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventory
from app.database import engine, Base
from app.models import inventory_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

@app.get("/health")
async def health():
    return {"status": "ok"}