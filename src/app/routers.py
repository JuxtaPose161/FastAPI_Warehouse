from time import sleep
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.models import Product, Order, Status, OrderItem
from src.app.operations import make_all_order_items, get_all_order_items
from src.app.schemas import ProductRead, OrderCreate, OrderUpdate, ProductCreate, OrderRead, ProductUpdate
from src.database import get_async_session

from fastapi_cache.decorator import cache

product_router = APIRouter(
    prefix='/products',
    tags=['Products']
)

order_router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

# cache
@product_router.get("/", response_model=List[ProductRead])
@cache(expire=10)
async def get_all_products(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Product))
    return result.scalars().all()

@product_router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_async_session)):
    product = Product(**product.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@product_router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    product = await db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return product

@product_router.put("/{product_id}", response_model=ProductRead)
async def change_product_info(product_id: int, product_data: ProductUpdate, db: AsyncSession = Depends(get_async_session)):
    product = await db.get(Product, product_id)
    for key, value in product_data.dict().items():
        setattr(product, key, value) if value else None
    await db.commit()
    await db.refresh(product)

    return product

@product_router.delete("/{product_id}", response_model=ProductRead)
async def delete_products(product_id: int, db: AsyncSession = Depends(get_async_session)):
    product = await db.get(Product, product_id)
    await db.delete(product)
    await db.commit()
    return product

# cache
@order_router.get("/", response_model=List[OrderRead])
@cache(expire=5)
async def get_all_orders(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Order).options(joinedload(Order.order_items)))
    return result.unique().scalars().all()

@order_router.post("/", response_model=OrderRead)
async def create_order(order_list: OrderCreate, db: AsyncSession = Depends(get_async_session)):
    row_order = Order(status=Status.in_progress)
    db.add(row_order)
    await make_all_order_items(db, order_list, row_order)
    await db.commit()
    await db.refresh(row_order)
    return await get_all_order_items(db, row_order)

@order_router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, db: AsyncSession = Depends(get_async_session)):
    row_order = await db.get(Order, order_id)
    return await get_all_order_items(db, row_order)
@order_router.patch("/{order_id}/status", response_model=OrderRead)
async def change_order_status(order_id: int, update: OrderUpdate, db: AsyncSession = Depends(get_async_session)):
    row_order = await db.get(Order, order_id)
    row_order.status = update.status
    await db.commit()
    await db.refresh(row_order)
    return await get_all_order_items(db, row_order)