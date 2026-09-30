from datetime import date

import httpx

from app.config import settings


class OpenMeteoClient:

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def get_daily_weather(
        self,
        start_date: date,
        end_date: date,
    ) -> dict:
        params = {
            "latitude": settings.weather_latitude,
            "longitude": settings.weather_longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": (
                "temperature_2m_mean,"
                "temperature_2m_min,"
                "temperature_2m_max,"
                "precipitation_sum"
            ),
            "timezone": "Europe/Kyiv",
        }

        response = httpx.get(
            self.BASE_URL,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()