from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class SQLiteConfig(BaseModel):
    name: str = "name"
    path: str = "path"
    echo: bool = False

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.path}/{self.name}.db"


class DatabaseConfig(BaseModel):
    type: str = "memory"
    sqlite: SQLiteConfig = SQLiteConfig()

    @property
    def connection_url(self) -> str:
        if self.type == "sqlite":
            return self.sqlite.url
        elif self.type == "memory":
            return "memory://"
        else:
            raise ValueError(f"Unsupported db_type: {self.type}")


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(
        env_file=(".env.dist", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = Settings()

# print(settings.db.type)
# print(settings.db.sqlite)
# print(settings.db.connection_url)