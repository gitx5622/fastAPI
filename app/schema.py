from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class Product(BaseModel):
    title: str
    image_url: str
    market_price: int
    selling_price: int
    description: str
    category_id: int
    date: datetime.date


class User(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
