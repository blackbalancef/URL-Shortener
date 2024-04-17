from shortuuid import ShortUUID
from fastapi import Request

from redis_cache.client import redis_client
from app.exception import NotFoundError
from app.link.crud import BaseCrud
from app.link.model import Link
from app.link.schema import LinkInput, ShortUrlResponse
from app.settings import app_settings
from app.utils import get_host_ip


def generate_short_link(prefix: str | None = None) -> str:
    return (f"{prefix}-" if prefix else "") + ShortUUID().random(length=6)


def enrich_link_with_host_name(host: str, link: str) -> str:
    return host + app_settings.LINK_ROUTER + "/" + link


class LinkService:
    def __init__(self, crud: BaseCrud):
        self.crud = crud

    async def cut_link(self, link: LinkInput, request: Request) -> ShortUrlResponse:
        client_ip = get_host_ip(request)
        short_url = generate_short_link(prefix=link.prefix)
        db_link = await self.crud.create(url=str(link.url), short_url=short_url)
        await redis_client.insert_cut_log(
            short_link=short_url, original_link=str(link.url), client_ip=client_ip
        )
        short_link = enrich_link_with_host_name(
            app_settings.host_prefix, db_link.short_url
        )
        return ShortUrlResponse(short_url=short_link)

    async def map_original_link(self, request: Request, short_link: str) -> str:
        original_link = await redis_client.get_cached_original_link(short_link)
        if original_link is None:
            db_link = await self.crud.get_by_field(short_url=short_link)
            original_link = db_link.url
        if original_link:
            client_ip = get_host_ip(request)
            await redis_client.insert_visit_log(
                short_link=short_link, original_link=original_link, client_ip=client_ip
            )
            return original_link
        else:
            raise NotFoundError(id_=original_link, object_=Link.__name__)
