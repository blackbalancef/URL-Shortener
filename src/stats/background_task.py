import asyncio
import json
from datetime import timedelta, UTC, datetime

from loguru import logger
from redis_cache.client import redis_client
from redis_cache.settings import redis_settings


async def update_popular_links() -> None:
    try:
        logger.info("Updating popular links")

        time_delta_ago = datetime.now(tz=UTC) - timedelta(
            minutes=redis_client.cache_time_size
        )
        time_delta_ago_timestamp = int(time_delta_ago.timestamp())

        visits = await redis_client.redis.zrangebyscore(
            "visits", time_delta_ago_timestamp, "+inf"
        )
        if not visits:
            return
        popular_links: dict[str, dict] = {}
        for visit_key in visits:
            visit_data = await redis_client.redis.hgetall(visit_key)
            short_url = visit_data["short_url"]
            original_url = visit_data["original_url"]

            if short_url in popular_links:
                popular_links[short_url]["count"] += 1
            else:
                popular_links[short_url] = {"original_url": original_url, "count": 1}

        sorted_popular_links = sorted(
            popular_links.items(), key=lambda x: x[1]["count"], reverse=True
        )[: redis_client.max_cached_links]

        if await redis_client.redis.exists("popular_links"):
            await redis_client.redis.delete("popular_links")

        for short_url, link_data in sorted_popular_links:
            await redis_client.redis.set(
                f"popular_links:{short_url}", json.dumps(link_data)
            )

        logger.info("Popular links updated")
    except Exception as e:
        logger.error(f"Error updating popular links: {e}", exc_info=True)


async def update_popular_links_task():
    while True:
        await update_popular_links()
        await asyncio.sleep(redis_settings.TTL_CACHE_POPULAR_LINKS)
