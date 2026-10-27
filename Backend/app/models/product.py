from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from app.db.session import Base

# ===============================================================
# id
# school_id
# name
# price_cents
# is_active
# created_at
# ===============================================================

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_id = Column(String, nullable=False, default="schule-1", index=True)
    
    name = Column(String, nullable=False)
    
    # Price stored as integer 
    price_cents = Column(Integer, nullable=False)
    
    # For deactivating deleted/sold-out products without losing DB entries
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())