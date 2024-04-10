from fastapi import APIRouter

from redis_cache.client import redis_client
from src.exception import NotFoundError

stats_router = APIRouter()


@stats_router.get("/stats/{short_link}")
async def link_stats(short_link: str):
    details = await redis_client.get_link_visit_stats(short_link)
    if details is not None:
        return details
    raise NotFoundError(id_=short_link, object_="Link")
