from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order_schema import OrderRequest, OrderResponse, OrderListResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["Order"])

# [POST] 결제 및 주문 생성
# 주소: POST /api/checkout
@router.post("/checkout", response_model=OrderResponse)
async def checkout(order: OrderRequest, db: Session = Depends(get_db)):
    return OrderService.process_checkout(db, order)

# [GET] 전체 주문 목록 조회
# 주소: GET /api/orders
@router.get("/orders", response_model=List[OrderListResponse])
async def get_orders(db: Session = Depends(get_db)):
    return OrderService.get_all_orders(db)

# [GET] 사용자별 주문 내역 조회 (마이페이지용)
# 주소: GET /api/orders/{user_id}
@router.get("/orders/{user_id}", response_model=List[OrderListResponse])
async def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    return OrderService.get_orders_by_user(db, user_id)

# [PATCH] 주문 취소 (환불 로직 포함)
# 주소: PATCH /api/orders/{order_id}
@router.patch("/orders/{order_id}", response_model=OrderListResponse)
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.cancel_order(db, order_id)