from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

# ---------------- USER TABLE ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ---------------- ITEM TABLE ----------------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    added_on = Column(DateTime(timezone=True), server_default=func.now())

    status = Column(String, default="active")
    notes = Column(String, nullable=True)
