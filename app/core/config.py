from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = """ возможность забронировать свободное помещение
        на определённый период времени, при этом приложение должно проверять, не
        забронировал ли уже кто-то это помещение и свободно ли всё время,
        на которое бронируется эта переговорка."""
    database_url: str

    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()