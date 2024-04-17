from fastapi import APIRouter
from fastapi import Depends, Request, status
from starlette.responses import RedirectResponse
from loguru import logger

from app.dependecies import get_service
from app.link.model import Link
from app.link.schema import LinkInput, ShortUrlResponse
from app.link.service import LinkService

link_router = APIRouter()


@link_router.post("/cut_link")
async def cut_link(
    request: Request,
    link: LinkInput,
    link_service: LinkService = Depends(get_service(LinkService, Link)),
) -> ShortUrlResponse:
    return await link_service.cut_link(link, request)


@link_router.get("/{short_link}", status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def redirect(
    request: Request,
    short_link: str,
    link_service: LinkService = Depends(get_service(LinkService, Link)),
) -> RedirectResponse:
    original_link = await link_service.map_original_link(request, short_link)
    logger.info(f"Redirecting to {original_link}")
    return RedirectResponse(
        url=original_link, status_code=status.HTTP_308_PERMANENT_REDIRECT
    )
