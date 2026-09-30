from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.weather import Weather
from app.api.weather import router as weather_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Rivne Weather Service",
)

app.include_router(weather_router)