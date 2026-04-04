from sqlalchemy import Column, Integer, String
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50))
    item_id = Column(String(50))
    price = Column(Integer)
    quantity = Column(Integer)
    status = Column(String(20))