from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.link.crud import BaseCrud
from db.session import get_session


def get_crud(model):
    async def crud_operations(session: AsyncSession = Depends(get_session)):
        return BaseCrud(session=session, model=model)

    return crud_operations


def get_service(service, model):
    async def service_operations(crud: BaseCrud = Depends(get_crud(model))):
        return service(crud)

    return service_operations
