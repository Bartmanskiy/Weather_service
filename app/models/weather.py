from datetime import date

from sqlalchemy import Date, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
    )

    temperature_avg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    temperature_min: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    temperature_max: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    precipitation: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
