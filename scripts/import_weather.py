from datetime import date, timedelta

from app.clients.open_meteo_client import OpenMeteoClient
from app.db.database import SessionLocal
from app.repositories.weather_repository import WeatherRepository
from app.services.weather_service import WeatherService
from app.cache.redis import get_redis


def main():
    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    db = SessionLocal()

    try:
        service = WeatherService(
            repository=WeatherRepository(db),
            client=OpenMeteoClient(),
            redis_client=get_redis(),
        )

        imported_count = service.import_weather(
            start_date,
            end_date,
        )

        print(
            f"Imported {imported_count} days "
            f"from {start_date} to {end_date}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()