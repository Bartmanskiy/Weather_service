import json
from datetime import date

from app.cache.redis import redis_client
from app.repositories.weather_analytics_repository import (
    WeatherAnalyticsRepository,
)


class AnalyticsService:

    def __init__(
        self,
        repository: WeatherAnalyticsRepository,
    ):
        self.repository = repository

    def get_average_for_period(
        self,
        start_date: date,
        end_date: date,
    ):
        cache_key = f"weather:average:{start_date}:{end_date}"

        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)

        average_temperature, total_precipitation = (
            self.repository.get_average_for_period(
                start_date,
                end_date,
            )
        )

        result = {
            "average_temperature": average_temperature,
            "total_precipitation": total_precipitation,
        }

        redis_client.set(
            cache_key,
            json.dumps(result),
            ex=3600,
        )

        return result

    def get_extremes(self):
        cache_key = "weather:extremes"

        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)

        minimum_temperature, maximum_temperature = self.repository.get_extremes()

        result = {
            "minimum_temperature": minimum_temperature,
            "maximum_temperature": maximum_temperature,
        }

        redis_client.set(
            cache_key,
            json.dumps(result),
            ex=3600,
        )

        return result

    def get_monthly_statistics(
        self,
        year: int,
        month: int,
    ):
        cache_key = f"weather:monthly:{year}:{month}"

        cached_result = redis_client.get(cache_key)

        if cached_result:
            return json.loads(cached_result)

        average_temperature, precipitation_days = (
            self.repository.get_monthly_statistics(
                year,
                month,
            )
        )

        result = {
            "average_temperature": average_temperature,
            "precipitation_days": precipitation_days,
        }

        redis_client.set(
            cache_key,
            json.dumps(result),
            ex=3600,
        )

        return result
