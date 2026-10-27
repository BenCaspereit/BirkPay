from sqlalchemy import Column, String, Integer, DateTime, func
from app.db.session import Base

# ================================================================
# id
# school_id
# nfc_uid
# name
# balance_cents
# role
# created_at
# ===============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_id = Column(String, nullable=False, default="schule-1", index=True)
    
    
    nfc_uid = Column(String, unique=True, nullable=True, index=True)
    name = Column(String, nullable=False)
    
    # Money saved as integer 
    balance_cents = Column(Integer, nullable=False, default=0)
    
    # roles: 'student', 'cashier', 'bank', 'admin'
    role = Column(String, nullable=False, default="student")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())