from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.wallet_service import WalletService

router = APIRouter(prefix="/api/orders/wallets", tags=["Wallet"])

@router.post("/{user_id}") # [서진] 회원가입 하면 정보를 받아와서 지갑 생성해주는 api
async def create_user_wallet(user_id: str, db: Session = Depends(get_db)):
    return WalletService.create_wallet(db, user_id)