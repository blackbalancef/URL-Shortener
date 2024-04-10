from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    HOST: str
    PORT: int

    @property
    def host_prefix(self):
        return f"http://{self.HOST}:{self.PORT}"


app_settings = AppSettings()
