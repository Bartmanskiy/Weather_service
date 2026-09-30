from datetime import date

from app.models.weather import Weather


def add_weather(db_session):
    db_session.add_all(
        [
            Weather(
                date=date(2025, 1, 1),
                temperature_avg=-2.0,
                temperature_min=-7.0,
                temperature_max=1.0,
                precipitation=3.0,
            ),
            Weather(
                date=date(2025, 1, 2),
                temperature_avg=2.0,
                temperature_min=-1.0,
                temperature_max=5.0,
                precipitation=5.0,
            ),
            Weather(
                date=date(2025, 1, 3),
                temperature_avg=6.0,
                temperature_min=2.0,
                temperature_max=9.0,
                precipitation=0.0,
            ),
        ]
    )

    db_session.commit()


def test_average_weather(client, db_session):
    add_weather(db_session)

    response = client.get(
        "/api/weather/average",
        params={
            "start_date": "2025-01-01",
            "end_date": "2025-01-03",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["average_temperature"] == 2.0
    assert data["total_precipitation"] == 8.0


def test_extreme_weather(client, db_session):
    add_weather(db_session)

    response = client.get(
        "/api/weather/extremes",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["minimum_temperature"] == -7.0
    assert data["maximum_temperature"] == 9.0


def test_monthly_weather(client, db_session):
    add_weather(db_session)

    response = client.get(
        "/api/weather/monthly/2025/1",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["average_temperature"] == 2.0
    assert data["precipitation_days"] == [1, 2]


def test_average_invalid_date_range(client):
    response = client.get(
        "/api/weather/average",
        params={
            "start_date": "2025-01-10",
            "end_date": "2025-01-01",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "start_date must be before or equal to end_date"
    )


def test_monthly_invalid_month(client):
    response = client.get(
        "/api/weather/monthly/2025/13",
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "month must be between 1 and 12"
    )