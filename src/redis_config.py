from typing import AsyncGenerator

import redis
from redis.asyncio import Redis

from config import REDIS_HOST, REDIS_PORT

redis_pool = redis.asyncio.ConnectionPool.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")


async def get_async_redis_client() -> AsyncGenerator[Redis, None]:
    async with Redis.from_pool(redis_pool) as client:
        print("start connection")
        yield client
        print("end_connection")


