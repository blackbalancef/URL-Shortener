import asyncio

from fastapi import FastAPI, status, Request
from starlette.responses import JSONResponse


from redis_cache.client import redis_client
from src.link.api_router import link_router
from src.exception import NotFoundError
from src.stats.api_router import stats_router
from src.stats.background_task import update_popular_links_task

app = FastAPI()

app.include_router(link_router, prefix="/link")
app.include_router(stats_router, prefix="/stats")


@app.on_event("startup")
async def startup_event():
    await redis_client.connect()
    asyncio.create_task(update_popular_links_task())


@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()


@app.exception_handler(NotFoundError)
async def not_found(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=exc.details)
