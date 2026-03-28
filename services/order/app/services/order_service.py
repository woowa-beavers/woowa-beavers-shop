from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.schemas.order_schema import OrderRequest, OrderStatus

class OrderService:
    @staticmethod
    def process_checkout(db: Session, order_data: OrderRequest):
        user_current_point = 1000000 
        
        # 총 결제 금액 계산
        total_price = order_data.price * order_data.quantity
        
        # 포인트 부족 검증
        if user_current_point < total_price:
            raise HTTPException(status_code=400, detail="포인트가 부족하여 결제에 실패했습니다.")

        new_order = Order(
            user_id=order_data.user_id,
            item_id=order_data.item_id,
            price=order_data.price,
            quantity=order_data.quantity,
            status=OrderStatus.PAID
        )

        # RDS 저장 명령
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # 결과 반환
        return {
            "order_id": new_order.id,
            "status": new_order.status,
            "message": "결제가 완료되었으며 RDS에 저장되었습니다.",
            "remaining_point": user_current_point - total_price
        }