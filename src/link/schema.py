from pydantic import BaseModel, AnyHttpUrl, Field


class LinkInput(BaseModel):
    url: AnyHttpUrl
    prefix: str | None = Field(..., pattern="^[a-z0-9]*$")


class ShortUrlResponse(BaseModel):
    short_url: AnyHttpUrl
