from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base schema for user-related data
class UserBase(BaseModel):
    name: str
    school_id: str = "schule-1"
    role: str = "student"

# Schema for creating a new user (POST /users)
class UserCreate(UserBase):
    nfc_uid: Optional[str] = None
    balance_cents: int = 0

# Schema for updates (PUT / PATCH /users/{id})
class UserUpdate(BaseModel):
    name: Optional[str] = None
    nfc_uid: Optional[str] = None
    role: Optional[str] = None
    balance_cents: Optional[int] = None

# Schema for responses (GET /users/{id})
class UserResponse(UserBase):
    id: int
    nfc_uid: Optional[str] = None
    balance_cents: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)