from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order_model import Order 
from app.models.wallet_model import Wallet
from app.schemas.order_schema import OrderRequest, OrderStatus

class OrderService:
    # [서연] 인벤토리 서버로부터 재고 불러오는 api로 대체
    MOCK_INVENTORY = {
        "beaver_item_01": 10,
        "beaver_item_02": 5
    }

    @staticmethod
    def process_checkout(db: Session, order_data: OrderRequest):
        # 포인트 조회 및 검증
        wallet = db.query(Wallet).filter(Wallet.user_id == order_data.user_id).first()
        
        if not wallet:
            raise HTTPException(
                status_code=404, 
                detail="지갑 정보가 없습니다. 회원가입 여부를 확인하세요."
            )
        
        total_price = order_data.price * order_data.quantity
        
        # 잔액 검증
        if wallet.balance < total_price:
            raise HTTPException(
                status_code=400, 
                detail=f"포인트가 부족합니다. (현재 잔액: {wallet.balance}원)"
            )

        # 2. 재고 검증 ([서연] 재고 api 호출 예정 - 현재는 Mock)
        current_stock = OrderService.MOCK_INVENTORY.get(order_data.item_id)
        if current_stock is None or current_stock < order_data.quantity:
            raise HTTPException(status_code=400, detail="재고가 부족합니다.")

        # 처리 및 저장
        wallet.balance -= total_price
        
        # [서연] 재고 차감
        OrderService.MOCK_INVENTORY[order_data.item_id] -= order_data.quantity

        # DB에 주문 확정 기록 저장
        new_order = Order(
            user_id=order_data.user_id,
            item_id=order_data.item_id,
            price=order_data.price,
            quantity=order_data.quantity,
            status=OrderStatus.PAID
        )

        db.add(new_order)
        db.commit()
        db.refresh(wallet)
        db.refresh(new_order)

        return {
            "order_id": new_order.id,
            "status": new_order.status,
            "message": "결제가 완료되었습니다.",
            "remaining_point": wallet.balance
        }

    # ... get_all_orders, cancel_order 등 나머지 함수도 Wallet 연동 방식으로 수정 필요 ...