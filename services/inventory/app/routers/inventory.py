from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory_model import Product
from app.schemas.inventory_schema import StockResponse, StockReduceRequest, StockReduceResponse

router = APIRouter()

@router.get("/{item_id}", response_model=StockResponse)
async def get_stock(item_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.item_id == item_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    return {"item_id": product.item_id, "name": product.name, "stock": product.stock}

@router.patch("/{item_id}", response_model=StockReduceResponse)
async def reduce_stock(item_id: str, request: StockReduceRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.item_id == item_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    if product.stock < request.quantity:
        raise HTTPException(status_code=400, detail=f"재고가 부족합니다. (현재 재고: {product.stock}개)")
    product.stock -= request.quantity
    db.commit()
    db.refresh(product)
    return {
        "item_id": item_id,
        "remaining_stock": product.stock,
        "message": "재고가 차감되었습니다."
    }