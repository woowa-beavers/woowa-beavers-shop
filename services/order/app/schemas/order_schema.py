from pydantic import BaseModel, Field
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"     # 결제 대기
    PAID = "PAID"           # 결제 완료
    FAILED = "FAILED"       # 결제 실패
    CANCELLED = "CANCELLED" # 주문 취소

# 클라이언트가 보낼 데이터 (요청)
class OrderRequest(BaseModel):
    user_id: str
    item_id: str
    price: int = Field(..., gt=0, description="상품 가격은 0보다 커야 합니다.")
    quantity: int = Field(..., gt=0, description="수량은 최소 1개 이상이어야 합니다.")

# 서버가 돌려줄 데이터 (응답)
class OrderResponse(BaseModel):
    order_id: int
    status: OrderStatus
    message: str
    remaining_point: int