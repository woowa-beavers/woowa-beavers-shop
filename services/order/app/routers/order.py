from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order_schema import OrderRequest, OrderResponse, OrderListResponse
from app.services.order_service import OrderService

router = APIRouter()

# [POST] 결제 및 주문 생성
@router.post("/checkout", response_model=OrderResponse)
async def checkout(order: OrderRequest, db: Session = Depends(get_db)):
    return OrderService.process_checkout(db, order)

# [GET] 주문 목록 조회
@router.get("/orders", response_model=List[OrderListResponse])
async def get_orders(db: Session = Depends(get_db)):
    return OrderService.get_all_orders(db)

# 사용자별 주문 내역 조회
@router.get("/orders/{user_id}", response_model=List[OrderListResponse])
async def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    return OrderService.get_orders_by_user(db, user_id)

# [PATCH] 주문 취소
@router.patch("/orders/{order_id}", response_model=OrderListResponse)
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    result = OrderService.cancel_order(db, order_id)
    return result

@router.post("/{user_id}") #[서진] 회원가입하면 회원 정보를 넘겨받아옴
async def create_user_wallet(user_id: str, db: Session = Depends(get_db)):
    return WalletService.create_wallet(db, user_id)