from datetime import date

from app.models.weather import Weather
from app.repositories.weather_repository import WeatherRepository


def test_create_and_get_by_date(db_session):
    repository = WeatherRepository(db_session)

    weather = Weather(
        date=date(2025, 5, 1),
        temperature_avg=10.0,
        temperature_min=5.0,
        temperature_max=15.0,
        precipitation=2.5,
    )

    created = repository.create(weather)

    result = repository.get_by_date(
        date(2025, 5, 1)
    )

    assert created.id is not None
    assert result is not None
    assert result.date == date(2025, 5, 1)
    assert result.temperature_avg == 10.0