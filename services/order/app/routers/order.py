from fastapi import APIRouter
from app.schemas.order_schema import OrderRequest, OrderResponse
from app.services.order_service import OrderService

router = APIRouter()

@router.post("/checkout", response_model=OrderResponse)
async def checkout(order: OrderRequest):
    result = OrderService.process_checkout(order)
    return result