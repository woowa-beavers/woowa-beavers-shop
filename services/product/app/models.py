# services/product/app/models.py
# Commerce RDS의 products 테이블 ORM 모델

from sqlalchemy import Column, Integer, String
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(String(50), unique=True, index=True, nullable=False)  # 상품 고유 코드 (예: beaver_item_01)
    name    = Column(String(100), nullable=False)                          # 상품명
    price   = Column(Integer, nullable=False)                              # 가격 (원 단위 정수)
    emoji   = Column(String(20))                                           # 상품 이모지 (없으면 빈칸 렌더링)
    stock   = Column(Integer, nullable=False, default=100)                 # 재고 수량
