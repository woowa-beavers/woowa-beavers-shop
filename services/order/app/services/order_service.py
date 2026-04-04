from fastapi import HTTPException
from sqlalchemy.orm import Session
import httpx
from app.models.order_model import Order
from app.models.user_model import User
from app.schemas.order_schema import OrderRequest, OrderStatus

INVENTORY_URL = "http://10.0.2.33:8000/inventory"

class OrderService:

    @staticmethod
    def process_checkout(db: Session, order_data: OrderRequest):
        user = db.query(User).filter(User.username == order_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="유저 정보가 없습니다.")

        total_price = order_data.price * order_data.quantity

        if user.balance < total_price:
            raise HTTPException(
                status_code=400,
                detail=f"포인트가 부족합니다. (현재 잔액: {user.balance}원)"
            )

        # 재고 조회
        with httpx.Client() as client:
            res = client.get(f"{INVENTORY_URL}/{order_data.item_id}")
            if res.status_code == 404:
                raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
            stock_data = res.json()
            if stock_data["stock"] < order_data.quantity:
                raise HTTPException(status_code=400, detail=f"재고가 부족합니다. (현재 재고: {stock_data['stock']}개)")

        # 재고 차감
        with httpx.Client() as client:
            res = client.patch(f"{INVENTORY_URL}/{order_data.item_id}", json={"quantity": order_data.quantity})
            if res.status_code != 200:
                raise HTTPException(status_code=500, detail="재고 차감 실패")

        user.balance -= total_price

        new_order = Order(
            user_id=order_data.user_id,
            item_id=order_data.item_id,
            price=order_data.price,
            quantity=order_data.quantity,
            status=OrderStatus.PAID
        )
        db.add(new_order)
        db.commit()
        db.refresh(user)
        db.refresh(new_order)

        return {
            "order_id": new_order.id,
            "status": new_order.status,
            "message": "결제가 완료되었습니다.",
            "remaining_point": user.balance
        }

    @staticmethod
    def get_all_orders(db: Session):
        return db.query(Order).all()

    @staticmethod
    def get_orders_by_user(db: Session, user_id: str):
        return db.query(Order).filter(Order.user_id == user_id).all()

    @staticmethod
    def cancel_order(db: Session, order_id: int):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")

        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="이미 취소된 주문입니다.")

        user = db.query(User).filter(User.username == order.user_id).first()
        if user:
            user.balance += order.price * order.quantity

        order.status = OrderStatus.CANCELLED
        db.commit()
        db.refresh(order)
        return order
