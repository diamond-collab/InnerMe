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
    db_name: str = ''
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    echo: bool = True

    @property
    def url(self):
        """Собираем полный URL для SQLAlchemy"""
        return (
            f'postgresql+asyncpg://'
            f'{self.user}:{self.password}@'
            f'{self.host}:{self.port}/'
            f'{self.db_name}'
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
