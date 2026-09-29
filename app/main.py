from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.weather import Weather


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Rivne Weather Service",
)