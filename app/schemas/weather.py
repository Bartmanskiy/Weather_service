from pydantic import BaseModel


class AverageWeatherResponse(BaseModel):
    average_temperature: float | None
    total_precipitation: float | None


class ExtremeWeatherResponse(BaseModel):
    minimum_temperature: float | None
    maximum_temperature: float | None


class MonthlyWeatherResponse(BaseModel):
    average_temperature: float | None
    precipitation_days: list[int]