from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.app.routers import product_router, order_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
app = FastAPI(
    title='Warehouse',
    lifespan=lifespan
)

app.include_router(product_router)
app.include_router(order_router)




