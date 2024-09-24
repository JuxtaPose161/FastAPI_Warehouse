from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.models import Product, OrderItem, Order
from src.app.schemas import OrderCreate


async def make_all_order_items(db: AsyncSession, order_list: OrderCreate, order: Order):
    all_items = []
    for product in order_list.order_items:
        obj = await db.get(Product, product.product_id)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"Product {product.product_id} not found")
        if obj.count < product.count:
            raise HTTPException(status_code=400, detail=f"Requested count {product.count} exceeds available count {obj.count}")
        obj.count -= product.count

        order_item = OrderItem(order_id=order.id, product_id=product.product_id, count=product.count)
        all_items.append(order_item)
    db.add_all(all_items)
    await db.commit()

async def get_all_order_items(db: AsyncSession, row_order: Order):
    result = await db.execute(
        select(Order)
        .where(Order.id == row_order.id)
        .options(joinedload(Order.order_items))
    )
    order = result.unique().scalars().one_or_none()
    return order