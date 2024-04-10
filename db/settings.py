from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    def _get_db_uri(self, scheme: str) -> str:
        """Return sync or async postgresql uri."""
        return str(
            PostgresDsn.build(
                scheme=scheme,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD.get_secret_value(),
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=f"{self.POSTGRES_DB}",
            )
        )

    @property
    def async_db_uri(self) -> str:
        return self._get_db_uri(scheme="postgresql+asyncpg")

    @property
    def sync_db_uri(self) -> str:
        return self._get_db_uri(scheme="postgresql")


db_settings = DBSettings()
