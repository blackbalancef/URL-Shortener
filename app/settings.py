from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    HOST: str
    PORT: int

    LINK_ROUTER: str = "/links"

    @property
    def host_prefix(self):
        return f"http://{self.HOST}:{self.PORT}"


app_settings = AppSettings()
