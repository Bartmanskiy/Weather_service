from datetime import date

from app.clients.open_meteo_client import OpenMeteoClient
from app.models.weather import Weather
from app.repositories.weather_repository import WeatherRepository


class WeatherService:

    def __init__(
        self,
        repository: WeatherRepository,
        client: OpenMeteoClient,
    ):
        self.repository = repository
        self.client = client

    def import_weather(
        self,
        start_date: date,
        end_date: date,
    ) -> int:
        data = self.client.get_daily_weather(
            start_date,
            end_date,
        )

        daily = data["daily"]

        weather_records = []

        for index, date_string in enumerate(daily["time"]):
            weather_date = date.fromisoformat(date_string)

            existing_weather = self.repository.get_by_date(
                weather_date
            )

            if existing_weather:
                continue

            weather = Weather(
                date=weather_date,
                temperature_avg=daily["temperature_2m_mean"][index],
                temperature_min=daily["temperature_2m_min"][index],
                temperature_max=daily["temperature_2m_max"][index],
                precipitation=daily["precipitation_sum"][index],
            )

            weather_records.append(weather)

        if not weather_records:
            return 0

        return self.repository.create_many(weather_records)