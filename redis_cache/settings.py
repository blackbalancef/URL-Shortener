from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    MAX_CACHE_SIZE: int = 10  # amount of links
    CACHE_TIME_SIZE: int = 60  # check last minutes for counting popular links
    TTL_CACHE_POPULAR_LINKS: int = 30  # seconds

    @property
    def host_prefix(self) -> str:
        return "redis://" + self.REDIS_HOST + ":" + str(self.REDIS_PORT)


redis_settings = RedisSettings()
