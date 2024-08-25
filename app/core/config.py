import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv('.env')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорных комнатя для предприятия'
    app_description: str = """Удобный и простой способ забронировать
    переговорную комнату для ваших встреч и совещаний. Наш сервис позволяет
    выбрать подходящее помещение, учитывая количество участников,
    дату и время встречи."""
    secret: str = Field(..., env='SECRET')
    db_host: str = Field(..., env='DB_HOST')
    db_port: str = Field(..., env='DB_PORT')
    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_pass: str = Field(..., env='DB_PASS')

    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}")


    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()