from datetime import date

from app.models.weather import Weather
from app.repositories.weather_analytics_repository import (
    WeatherAnalyticsRepository,
)


def add_weather(db_session):
    db_session.add_all(
        [
            Weather(
                date=date(2025, 1, 1),
                temperature_avg=-2.0,
                temperature_min=-7.0,
                temperature_max=1.0,
                precipitation=3.0,
            ),
            Weather(
                date=date(2025, 1, 2),
                temperature_avg=2.0,
                temperature_min=-1.0,
                temperature_max=5.0,
                precipitation=5.0,
            ),
            Weather(
                date=date(2025, 1, 3),
                temperature_avg=6.0,
                temperature_min=2.0,
                temperature_max=9.0,
                precipitation=0.0,
            ),
        ]
    )

    db_session.commit()


def test_get_average_for_period(db_session):
    add_weather(db_session)

    repository = WeatherAnalyticsRepository(db_session)

    average, precipitation = (
        repository.get_average_for_period(
            date(2025, 1, 1),
            date(2025, 1, 3),
        )
    )

    assert average == 2.0
    assert precipitation == 8.0


def test_get_extremes(db_session):
    add_weather(db_session)

    repository = WeatherAnalyticsRepository(db_session)

    minimum, maximum = repository.get_extremes()

    assert minimum == -7.0
    assert maximum == 9.0


def test_get_monthly_statistics(db_session):
    add_weather(db_session)

    repository = WeatherAnalyticsRepository(db_session)

    average, precipitation_days = (
        repository.get_monthly_statistics(
            2025,
            1,
        )
    )

    assert average == 2.0
    assert precipitation_days == [1, 2]