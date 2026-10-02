from datetime import date

from app.models.weather import Weather
from app.repositories.weather_repository import WeatherRepository
from app.services.weather_service import WeatherService


class FakeWeatherClient:

    def get_daily_weather(self, start_date, end_date):
        return {
            "daily": {
                "time": [
                    "2025-06-01",
                    "2025-06-02",
                ],
                "temperature_2m_mean": [
                    15.0,
                    18.0,
                ],
                "temperature_2m_min": [
                    10.0,
                    13.0,
                ],
                "temperature_2m_max": [
                    20.0,
                    23.0,
                ],
                "precipitation_sum": [
                    2.0,
                    0.0,
                ],
            }
        }


def test_import_weather(db_session, fake_redis):
    service = WeatherService(
        repository=WeatherRepository(db_session),
        client=FakeWeatherClient(),
        redis_client=fake_redis,
    )

    imported_count = service.import_weather(
        date(2025, 6, 1),
        date(2025, 6, 2),
    )

    assert imported_count == 2

    weather = db_session.query(Weather).all()

    assert len(weather) == 2
    assert weather[0].date == date(2025, 6, 1)
    assert weather[0].temperature_avg == 15.0


def test_import_weather_skips_duplicates(db_session, fake_redis):
    service = WeatherService(
        repository=WeatherRepository(db_session),
        client=FakeWeatherClient(),
        redis_client=fake_redis,
    )

    first_import = service.import_weather(
        date(2025, 6, 1),
        date(2025, 6, 2),
    )

    second_import = service.import_weather(
        date(2025, 6, 1),
        date(2025, 6, 2),
    )

    assert first_import == 2
    assert second_import == 0

    weather = db_session.query(Weather).all()

    assert len(weather) == 2


def test_import_weather_invalidates_cache(db_session, fake_redis):
    fake_redis.set(
        "weather:average:2025-06-01:2025-06-02",
        '{"average_temperature": 20}',
    )

    fake_redis.set(
        "weather:extremes",
        '{"minimum_temperature": 10}',
    )

    fake_redis.set(
        "other:key",
        "keep me",
    )

    service = WeatherService(
        repository=WeatherRepository(db_session),
        client=FakeWeatherClient(),
        redis_client=fake_redis,
    )

    imported_count = service.import_weather(
        date(2025, 6, 1),
        date(2025, 6, 2),
    )

    assert imported_count == 2

    assert fake_redis.get(
        "weather:average:2025-06-01:2025-06-02"
    ) is None

    assert fake_redis.get(
        "weather:extremes"
    ) is None

    assert fake_redis.get("other:key") == "keep me"