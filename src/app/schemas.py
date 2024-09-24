from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from src.app.models import Status


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] | None = None
    count: int = Field(gt=0)

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str] | None = None
    count: Optional[int] | None = Field(None, gt=0)

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] | None = None
    count: int = Field(gt=0)


    model_config = ConfigDict(from_attributes=True)

class ProductItem(BaseModel):
    product_id: int
    count: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    order_items: List[ProductItem]

class OrderUpdate(BaseModel):
    status: Status

class OrderRead(BaseModel):
    id: int
    order_items: List[ProductItem]
    created_at: datetime
    status: Status

    model_config = ConfigDict(from_attributes=True)