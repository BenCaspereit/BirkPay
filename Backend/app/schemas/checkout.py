from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

# single item in the shopping cart
class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Menge muss mindestens 1 sein")

# request body for checkout endpoint
class CheckoutRequest(BaseModel):
    nfc_uid: str
    items: List[CartItem]
    cashier_user_id: Optional[int] = None 

# response schema for successful checkout
class CheckoutResponse(BaseModel):
    success: bool
    transaction_id: int
    user_id: int
    user_name: str
    total_amount_cents: int
    new_balance_cents: int
    timestamp: datetime

# response schema for transaction history
class TransactionResponse(BaseModel):
    id: int
    school_id: str
    user_id: int
    amount_cents: int
    type: str
    created_by_user_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)