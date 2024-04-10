from fastapi import APIRouter
from fastapi import Depends, Request
from starlette.responses import RedirectResponse
from loguru import logger

from redis_cache.client import redis_client
from src.link.crud import BaseCrud
from src.dependecies import get_crud, get_service
from src.exception import NotFoundError
from src.link.model import Link
from src.link.schema import LinkInput, ShortUrlResponse
from src.link.service import LinkService, generate_short_link
from src.settings import app_settings
from src.utils import get_host_ip

link_router = APIRouter()


@link_router.post("/cut_link", response_model=ShortUrlResponse)
async def cut_link(
    request: Request,
    link: LinkInput,
    link_service: LinkService = Depends(get_service(LinkService, Link)),
) -> Link:
    client_ip = get_host_ip(request)
    short_url = generate_short_link(prefix=link.prefix)
    db_link = await link_service.crud.create(url=str(link.url), short_url=short_url)
    await redis_client.insert_cut_log(
        short_link=short_url, original_link=str(link.url), client_ip=client_ip
    )
    db_link.short_url = app_settings.host_prefix + "/link/" + db_link.short_url
    return db_link


@link_router.get("/{short_link}")
async def redirect(
    request: Request, short_link: str, crud: BaseCrud = Depends(get_crud(Link))
) -> RedirectResponse:
    original_link = await redis_client.get_cached_original_link(short_link)
    if original_link is None:
        db_link = await crud.get_by_field(short_url=short_link)
        original_link = db_link.url
    if original_link:
        client_ip = get_host_ip(request)
        await redis_client.insert_visit_log(
            short_link=short_link, original_link=original_link, client_ip=client_ip
        )
        logger.info(f"Redirecting to {original_link}")
        return RedirectResponse(url=original_link)
    else:
        raise NotFoundError(id_=original_link, object_=Link.__name__)
