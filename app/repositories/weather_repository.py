from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weather import Weather


class WeatherRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, weather: Weather) -> Weather:
        self.db.add(weather)
        self.db.commit()
        self.db.refresh(weather)

        return weather

    def create_many(self, weather_records: list[Weather]) -> int:
        self.db.add_all(weather_records)
        self.db.commit()

        return len(weather_records)
    

    def get_by_date(self, weather_date: date) -> Weather | None:
        statement = select(Weather).where(
            Weather.date == weather_date
        )

        return self.db.scalar(statement)