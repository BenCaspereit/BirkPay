from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price_cents: int
    school_id: str = "schule-1"

# Base schema for product-related data
class ProductCreate(ProductBase):
    pass

# Schema for updates (PUT /products/{id})
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price_cents: Optional[int] = None
    is_active: Optional[bool] = None

# Schema for responses (GET /products/{id})
class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)