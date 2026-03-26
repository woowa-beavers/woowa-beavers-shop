from sqlalchemy import Column, Integer, String
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False) # [서진] 회원가입 유저 ID랑 매칭
    balance = Column(Integer, default=1000000) # 가입 시 100만 포인트 기본 할당