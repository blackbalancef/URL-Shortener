from shortuuid import ShortUUID

from src.link.crud import BaseCrud
from src.link.model import Link
from src.link.schema import LinkInput


def generate_short_link(prefix: str | None = None) -> str:
    return (f"{prefix}-" if prefix else "") + ShortUUID().random(length=6)


class LinkService:
    def __init__(self, crud: BaseCrud):
        self.crud = crud

    async def make_short_link(self, link: LinkInput) -> Link:
        short_url = generate_short_link(prefix=link.prefix)
        return await self.crud.create(url=str(link.url), short_url=short_url)
