from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.weather_analytics_repository import WeatherAnalyticsRepository

from app.schemas.weather import AverageWeatherResponse, ExtremeWeatherResponse, MonthlyWeatherResponse
from app.services.analytics_service import AnalyticsService

from app.cache.redis import get_redis


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"],
)


@router.get(
    "/average",
    response_model=AverageWeatherResponse,
)
def get_average_weather(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis),
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date",
        )

    service = AnalyticsService(
        WeatherAnalyticsRepository(db),
        redis_client,
    )

    return service.get_average_for_period(
        start_date,
        end_date,
    )


@router.get(
    "/extremes",
    response_model=ExtremeWeatherResponse,
)
def get_extreme_weather(
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis),
):
    service = AnalyticsService(
        WeatherAnalyticsRepository(db),
        redis_client,
    )

    return service.get_extremes()


@router.get(
    "/monthly/{year}/{month}",
    response_model=MonthlyWeatherResponse,
)
def get_monthly_weather(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis),
):
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=400,
            detail="month must be between 1 and 12",
        )

    service = AnalyticsService(
        WeatherAnalyticsRepository(db),
        redis_client,
    )

    return service.get_monthly_statistics(
        year,
        month,
    )