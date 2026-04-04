from pydantic import BaseModel, Field

class StockResponse(BaseModel):
    item_id: str
    name: str
    stock: int

class StockReduceRequest(BaseModel):
    quantity: int = Field(..., gt=0, description="차감할 수량은 1 이상이어야 합니다.")

class StockReduceResponse(BaseModel):
    item_id: str
    remaining_stock: int
    message: str