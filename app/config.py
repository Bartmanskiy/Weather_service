from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_port: int = 8000

    database_url: str

    redis_host: str = "localhost"
    redis_port: int = 6379

    weather_city: str = "Rivne"
    weather_country_code: str = "UA"
    weather_latitude: float | None = None
    weather_longitude: float | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()