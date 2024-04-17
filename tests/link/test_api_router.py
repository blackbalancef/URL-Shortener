from typing import AsyncGenerator

import pytest
from fastapi import status
from dotenv import load_dotenv
from httpx import AsyncClient
from pydantic import AnyHttpUrl
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

from app.link.model import Base  # noqa: E402
from db.session import get_session  # noqa: E402
from db.settings import db_settings  # noqa: E402
from app.link.schema import ShortUrlResponse  # noqa: E402


from app.main import app  # noqa: E402
from app.settings import app_settings  # noqa: E402

test_engine = create_async_engine(
    url=db_settings.async_db_uri, echo=True, future=True, poolclass=NullPool
)
TestSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def db_test() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture()
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async def get_session_override():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


async def test_cut_link_200ok(async_client: AsyncClient):
    test_request_data = {"url": "https://example.com", "prefix": "test"}

    expected_short_url = f"{app_settings.host_prefix}/links/test"

    response = await async_client.post(
        f"{app_settings.LINK_ROUTER}/cut_link", json=test_request_data
    )

    # check response
    assert response.status_code == status.HTTP_200_OK
    response_schema = ShortUrlResponse.model_validate(response.json())
    expected_schema = ShortUrlResponse(short_url=AnyHttpUrl(expected_short_url))
    assert str(expected_schema.short_url) in str(response_schema.short_url)


async def test_cut_link_422(async_client: AsyncClient):
    test_request_data = {"url": "https://example.com", "prefix": "more_than10digits"}
    response = await async_client.post(
        f"{app_settings.LINK_ROUTER}/cut_link", json=test_request_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
