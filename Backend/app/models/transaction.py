from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from app.db.session import Base

# ===============================================================
# id
# school_id
# user_id
# amount_cents
# type
# created_by_user_id
# created_at
# ===============================================================

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_id = Column(String, nullable=False, default="schule-1", index=True)
    
    # link to the user who made the transaction
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Amount as integer:
    # - negative when debited (z.B. -350)
    # - positive when credited (z.B. +1000)
    amount_cents = Column(Integer, nullable=False)
    
    # Types: 'PURCHASE', 'DEPOSIT', 'SALARY', 'REFUND'
    type = Column(String, nullable=False)
    
    # Optional: Link to the user who created the transaction (e.g., cashier or bank)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)