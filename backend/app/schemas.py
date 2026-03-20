from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---------------- USER ----------------
class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


# ---------------- TOKEN ----------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------------- ITEM ----------------
class ItemCreate(BaseModel):
    name: str
    category: str
    expiry_date: datetime
    notes: Optional[str] = None


class ItemOut(BaseModel):
    id: int
    name: str
    category: str
    expiry_date: datetime
    status: str

    class Config:
        from_attributes = True
