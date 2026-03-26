from pydantic import BaseModel

# 클라이언트(프론트엔드나 유저)가 결제를 요청할 때 보내야 하는 데이터 형태
class OrderRequest(BaseModel):
    user_id: str      # 구매하는 유저의 고유 ID
    item_id: str      # 구매하려는 상품의 고유 ID
    price: int        # 상품의 개당 가격
    quantity: int     # 구매 수량

# 결제가 끝난 후 서버가 클라이언트에게 돌려줄 응답 데이터의 형태
class OrderResponse(BaseModel):
    status: str           # 결제 성공/실패 상태 (예: "success")
    message: str          # 처리 결과 안내 메시지
    remaining_point: int  # 결제 후 깎이고 남은 포인트 잔액