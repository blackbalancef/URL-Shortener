from fastapi import APIRouter

from redis_cache.client import redis_client
from app.stats.schema import Statistics

stats_router = APIRouter()


@stats_router.get("/stats/{short_link}")
async def link_stats(short_link: str) -> Statistics:
    return await redis_client.get_link_visit_stats(short_link)
