from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.exception import NotFoundError

Model = TypeVar("Model", bound=DeclarativeBase)


class BaseCrud(Generic[Model]):
    def __init__(self, session: AsyncSession, model: Model):
        self.session = session
        self.model = model

    async def get_by_id(self, id_: int) -> Model:
        result = await self.session.get(self.model, id_)
        if result is None:
            raise NotFoundError(id_=id_, object_=self.model.__name__)

    async def get_by_field(self, **kwargs) -> Model:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        db_obj = result.scalars().first()
        if db_obj is not None:
            return db_obj
        raise NotFoundError(object_=self.model.__name__)

    async def create(self, **kwargs) -> Model:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
