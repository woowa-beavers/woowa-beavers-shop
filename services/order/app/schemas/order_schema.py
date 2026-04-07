from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class OrderStatus(str, Enum):
    PENDING = "PENDING"     # 결제 대기
    PAID = "PAID"           # 결제 완료
    FAILED = "FAILED"       # 결제 실패
    CANCELLED = "CANCELLED" # 주문 취소

# 주문 생성 요청(Input)
class OrderRequest(BaseModel):
    user_id: str
    item_id: str
    price: int = Field(..., gt=0, description="상품 가격은 0보다 커야 합니다.")
    quantity: int = Field(..., gt=0, description="수량은 최소 1개 이상이어야 합니다.")

# 주문 완료 결과 반환 (POST /checkout)
class OrderResponse(BaseModel):
    order_id: int
    status: OrderStatus
    message: str
    remaining_point: int

# 주문 목록 조회 반환 (GET /orders)
class OrderListResponse(BaseModel):
    id: int
    user_id: str
    item_id: str
    price: int
    quantity: int
    status: OrderStatus

    class Config:
        from_attributes = True