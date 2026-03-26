from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Commerce RDS에 생성될 'orders' 테이블의 구조를 정의
class Order(Base):
    __tablename__ = "orders"

    # 기본키(PK): 주문 고유 번호
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 주문한 유저 ID와 상품 ID
    user_id = Column(String(50), index=True, nullable=False)
    item_id = Column(String(50), index=True, nullable=False)
    
    # 결제 정보
    price = Column(Integer, nullable=False)      # 개당 가격
    quantity = Column(Integer, nullable=False)   # 수량
    total_price = Column(Integer, nullable=False) # 총 결제 금액 (price * quantity)
    
    # 결제 상태 (예: "결제완료", "취소됨" 등)
    status = Column(String(20), default="결제완료")
    
    # 주문 생성 시간
    created_at = Column(DateTime, default=datetime.utcnow)

# [참고] 포인트 테이블에 대하여:
# 설계상 Auth RDS에 users 테이블이 있지만, 
# 결제할 때마다 통신을 줄이기 위해 Commerce RDS 쪽에 'user_points' 같은 별도 테이블을 만들거나,
# 나중에 User 서비스(EC2-2) 쪽으로 API를 쏴서 포인트를 차감하는 구조로 발전시킬 수 있어.
# 지금은 가장 핵심인 '주문 내역' 테이블만 먼저 정의