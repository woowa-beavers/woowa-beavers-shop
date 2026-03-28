from sqlalchemy.orm import Session
from app.models.wallet_model import Wallet
from fastapi import HTTPException

class WalletService:
    @staticmethod
    def create_wallet(db: Session, user_id: str):
        # 이미 지갑이 있는지 확인 (중복 가입 방지)
        existing_wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if existing_wallet:
            raise HTTPException(status_code=400, detail="이미 지갑이 존재하는 유저입니다.")

        # 새 지갑 생성
        new_wallet = Wallet(user_id=user_id, balance=1000000)
        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)
        return new_wallet

    @staticmethod
    def get_balance(db: Session, user_id: str):
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="지갑을 찾을 수 없습니다.")
        return wallet.balance