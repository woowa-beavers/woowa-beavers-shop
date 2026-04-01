from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.wallet_service import WalletService

router = APIRouter(prefix="/api/wallets", tags=["Wallet"])

@router.post("/{user_id}")
async def create_user_wallet(user_id: str, db: Session = Depends(get_db)):
    return WalletService.create_wallet(db, user_id)