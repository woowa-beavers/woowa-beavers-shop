from sqlalchemy import Column, Integer, String
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    emoji = Column(String(20))
    stock = Column(Integer, default=100)