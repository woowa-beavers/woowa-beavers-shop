from fastapi import APIRouter, HTTPException
from app.schemas.order_schema import OrderRequest, OrderResponse

router = APIRouter()

# 임시 메모리 DB (실제 배포할 때는 AWS의 Commerce RDS와 연결)
mock_user_db = {
    "user123": {"point": 1000000}
}

# 결제(checkout)를 처리하는 API 주소. POST 방식으로 "/checkout"에 요청이 오면 실행
@router.post("/checkout", response_model=OrderResponse)
async def checkout(order: OrderRequest):
    # 주문을 요청한 유저의 정보를 찾아옴(지금은 임시 DB에서 조회)
    user = mock_user_db.get(order.user_id)
    
    # 유저 정보가 없으면 404(Not Found)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 총 결제 금액 계산 = (상품 가격 * 구매 수량)
    total_price = order.price * order.quantity
    
    # 포인트 잔액 검증
    if user["point"] < total_price:
        raise HTTPException(status_code=400, detail="포인트가 부족합니다.")
    
    # 결제 금액만큼 유저의 포인트를 차감
    user["point"] -= total_price
    
    # 차후에 추가해야 할 작업들:
    # 1. Commerce RDS의 주문(orders) 테이블에 실제 주문 내역을 저장(INSERT)
    # 2. 재고 관리 서버(EC2-3)의 API를 호출해서 팔린 만큼 물건 재고를 감소
    
    # 결제가 성공 + 남은 포인트를 반환
    return OrderResponse(
        status="success", 
        message="결제가 완료되었으며 포인트가 차감되었습니다.", 
        remaining_point=user["point"]
    )