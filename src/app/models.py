import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)
    count: Mapped[int] = mapped_column(Integer)

    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
class Status(enum.Enum):
    in_progress = 'in_progress'
    sent = 'sent'
    delivered = 'delivered'

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[Status]

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete="CASCADE"))
    count: Mapped[int] = mapped_column(Integer)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")