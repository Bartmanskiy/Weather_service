from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.weather import router as weather_router
from app.db.database import Base, engine
from app.models.weather import Weather


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Rivne Weather Service",
    lifespan=lifespan,
)

app.include_router(weather_router)