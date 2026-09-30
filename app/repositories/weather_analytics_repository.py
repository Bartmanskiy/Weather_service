from datetime import date

from sqlalchemy import func, select, extract
from sqlalchemy.orm import Session

from app.models.weather import Weather


class WeatherAnalyticsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_average_for_period(
        self,
        start_date: date,
        end_date: date,
    ):
        statement = select(
            func.avg(Weather.temperature_avg),
            func.sum(Weather.precipitation),
        ).where(
            Weather.date >= start_date,
            Weather.date <= end_date,
        )

        return self.db.execute(statement).one()

    def get_extremes(self):
        statement = select(
            func.min(Weather.temperature_min),
            func.max(Weather.temperature_max),
        )

        return self.db.execute(statement).one()

    def get_monthly_statistics(
        self,
        year: int,
        month: int,
    ):
        average_statement = select(
            func.avg(Weather.temperature_avg)
        ).where(
            extract("year", Weather.date) == year,
            extract("month", Weather.date) == month,
        )

        precipitation_statement = select(
            extract("day", Weather.date)
        ).where(
            extract("year", Weather.date) == year,
            extract("month", Weather.date) == month,
            Weather.precipitation > 0,
        ).order_by(
            Weather.date
        )

        average_temperature = self.db.scalar(
            average_statement
        )

        precipitation_days = self.db.scalars(
            precipitation_statement
        ).all()

        return average_temperature, [
            int(day) for day in precipitation_days
        ]