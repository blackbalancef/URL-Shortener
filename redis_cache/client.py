import json
from collections import defaultdict
from datetime import datetime, UTC

import redis.asyncio as aioredis
from loguru import logger

from redis_cache.settings import redis_settings, RedisSettings
from app.exception import NotFoundError


class RedisClient:
    def __init__(self, redis_settings: RedisSettings):
        self.redis_url = redis_settings.host_prefix
        self.max_cached_links = redis_settings.MAX_CACHE_SIZE
        self.ttl_popular_links = redis_settings.TTL_CACHE_POPULAR_LINKS
        self.cache_time_size = redis_settings.CACHE_TIME_SIZE
        self.redis: aioredis.Redis

    async def connect(self):
        self.redis = aioredis.from_url(
            self.redis_url, encoding="utf-8", decode_responses=True
        )
        logger.info("Redis successfully connected")

    async def close(self):
        self.redis.close()
        logger.info("Redis shut down")

    async def insert_cut_log(self, short_link: str, original_link: str, client_ip: str):
        time_stamp = int(datetime.now(tz=UTC).timestamp())
        cutting_key = f"cuts:{short_link}:{time_stamp}"
        try:
            await self.redis.hmset(
                cutting_key,
                {
                    "short_url": short_link,
                    "original_url": original_link,
                    "ip": client_ip,
                    "timestamp": time_stamp,
                },
            )
        except Exception as e:
            logger.error(f"Error saving cutting for {short_link}: {e}")

    async def insert_visit_log(
        self, short_link: str, original_link: str, client_ip: str
    ):
        time_stamp = int(datetime.now(tz=UTC).timestamp())
        visit_key = f"{short_link}:{time_stamp}"

        await self.redis.zadd("visits", {visit_key: time_stamp})

        await self.redis.hmset(
            visit_key,
            {
                "short_url": short_link,
                "original_url": original_link,
                "ip": client_ip,
                "timestamp": time_stamp,
            },
        )

    async def get_cached_original_link(self, short_url: str) -> str | None:
        key = f"popular_links:{short_url}"
        if await self.redis.exists(key):
            stats = await self.redis.get(key)
            if stats:
                stats_dict = json.loads(stats)
                return stats_dict.get("original_url")
        return None

    async def get_link_visit_stats(self, short_link: str) -> dict[str, int]:
        pattern = f"{short_link}:*"

        cursor = "0"
        matches = []
        while cursor != 0:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)
            matches.extend(keys)
        if not matches:
            raise NotFoundError(id_=short_link, object_="Link")
        visits = []
        for visit_key in matches:
            visit_data = await self.redis.hgetall(visit_key)
            visits.append(visit_data)

        stats = {
            "total_visits": len(visits),
            "visits_by_date": defaultdict(int),
            "visits_by_hour": defaultdict(int),
        }

        for visit in visits:
            timestamp = visit.get("timestamp")
            if timestamp:
                visit_time = datetime.fromtimestamp(int(timestamp))
                visit_date = visit_time.strftime("%Y-%m-%d")
                visit_hour = visit_time.strftime("%H:00")

                stats["visits_by_date"][visit_date] += 1
                stats["visits_by_hour"][visit_hour] += 1

        stats["visits_by_date"] = dict(stats["visits_by_date"])
        stats["visits_by_hour"] = dict(stats["visits_by_hour"])

        return stats


redis_client = RedisClient(redis_settings)
