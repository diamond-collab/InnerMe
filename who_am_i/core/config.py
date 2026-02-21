from typing import Literal
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LoggingConfig(BaseModel):
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level: Literal[
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
    ] = 'INFO'


class DatabaseConfig(BaseModel):
    name: str = ''
    host: str = ''
    port: int = 1
    user: str = ''
    password: str = ''

    # echo: bool = True

    @property
    def url(self):
        """Собираем полный URL для SQLAlchemy"""
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'
        )


class BotConfig(BaseModel):
    token: str = ''


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )

    db: DatabaseConfig = DatabaseConfig()

    bot: BotConfig = BotConfig()

    logging: LoggingConfig = LoggingConfig()


settings = Settings()
