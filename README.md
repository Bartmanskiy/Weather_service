# Rivne Weather Service

REST API сервіс для зберігання та аналізу історичних даних про погоду для міста Рівне.

Проєкт побудований на **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis** та **Docker Compose**.

Дані про погоду отримуються з **Open-Meteo API**, зберігаються в PostgreSQL та використовуються для подальших аналітичних запитів.

---

## Основний функціонал

Сервіс підтримує:

* імпорт історичних даних про погоду з Open-Meteo;
* збереження температури та опадів у PostgreSQL;
* розрахунок середньої температури за заданий період;
* розрахунок загальної кількості опадів за період;
* пошук мінімальної та максимальної температури;
* отримання статистики за конкретний місяць;
* визначення днів місяця, коли були опади;
* кешування важких аналітичних запитів через Redis;
* валідацію вхідних даних;
* автоматизоване тестування;
* запуск усіх компонентів через Docker Compose.

---

## Технології

* **Python 3.11**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL 15**
* **Redis 7**
* **Pydantic Settings**
* **httpx**
* **pytest**
* **Docker**
* **Docker Compose**

---

## Архітектура

Проєкт використовує розділення відповідальності між окремими шарами:

```text
API
 │
 ▼
Service
 │
 ├── Repository ──► PostgreSQL
 │
 └── Redis Cache
```

Для отримання зовнішніх даних використовується окремий клієнт:

```text
Open-Meteo API
      │
      ▼
OpenMeteoClient
      │
      ▼
WeatherService
      │
      ▼
WeatherRepository
      │
      ▼
PostgreSQL
```

### Основні компоненти

* **API** — приймає HTTP-запити та повертає відповіді.
* **Services** — містять бізнес-логіку.
* **Repositories** — працюють з базою даних.
* **OpenMeteoClient** — відповідає тільки за отримання даних із зовнішнього API.
* **Redis** — кешує результати аналітичних запитів.
* **PostgreSQL** — основне сховище даних.

Такий підхід дозволяє не змішувати HTTP, бізнес-логіку та роботу з базою даних.

---

## Структура проєкту

```text
Weather_service/
├── app/
│   ├── api/
│   │   └── weather.py
│   ├── cache/
│   │   └── redis.py
│   ├── clients/
│   │   └── open_meteo_client.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── weather.py
│   ├── repositories/
│   │   ├── weather_repository.py
│   │   └── weather_analytics_repository.py
│   ├── schemas/
│   │   └── weather.py
│   ├── services/
│   │   ├── weather_service.py
│   │   └── analytics_service.py
│   ├── config.py
│   └── main.py
│
├── scripts/
│   └── import_weather.py
│
├── tests/
│   ├── conftest.py
│   ├── test_weather_repository.py
│   ├── test_weather_analytics_repository.py
│   ├── test_weather_service.py
│   └── test_weather_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## Налаштування

Для запуску необхідно створити `.env` на основі `.env.example`.

Приклад:

```env
API_PORT=8000

POSTGRES_USER=weather_user
POSTGRES_PASSWORD=weather_password
POSTGRES_DB=weather_db

REDIS_PORT=6379

WEATHER_CITY=Rivne
WEATHER_COUNTRY_CODE=UA
WEATHER_LATITUDE=50.6199
WEATHER_LONGITUDE=26.2516

DATABASE_URL=postgresql+psycopg2://weather_user:weather_password@localhost:5433/weather_db
```

Файл `.env` не додається до Git, оскільки він містить конфігурацію локального середовища.

---

## Запуск через Docker

Для запуску всіх компонентів:

```bash
docker compose up -d --build
```

Перевірити стан контейнерів:

```bash
docker compose ps
```

У проєкті запускаються три основні сервіси:

```text
api    → FastAPI
db     → PostgreSQL
cache  → Redis
```

API доступний за адресою:

```text
http://localhost:8000
```

Swagger документація:

```text
http://localhost:8000/docs
```

---

## Імпорт даних про погоду

Для імпорту історичних даних використовується Open-Meteo Archive API.

Запуск CLI-скрипта локально:

```bash
python -m scripts.import_weather
```

Скрипт:

1. визначає поточну дату;
2. формує період історичних даних;
3. отримує дані з Open-Meteo;
4. перевіряє, чи існує дата в PostgreSQL;
5. додає тільки відсутні записи.

Повторний запуск не створює дублікати.

Наприклад:

```text
Imported 0 days from 2025-09-30 to 2026-09-30
```

означає, що всі записи за цей період уже присутні в базі.

---

# API

Base URL:

```text
http://localhost:8000/api/weather
```

## 1. Середня температура та опади за період

```http
GET /api/weather/average
```

Параметри:

* `start_date`
* `end_date`

Приклад:

```text
GET /api/weather/average?start_date=2026-01-01&end_date=2026-01-31
```

Приклад відповіді:

```json
{
  "average_temperature": -7.661290322580644,
  "total_precipitation": 48.80000000000001
}
```

Розрахунок виконується безпосередньо в PostgreSQL за допомогою SQLAlchemy.

---

## 2. Мінімальна та максимальна температура

```http
GET /api/weather/extremes
```

Приклад відповіді:

```json
{
  "minimum_temperature": -25.3,
  "maximum_temperature": 38.4
}
```

---

## 3. Статистика за місяць

```http
GET /api/weather/monthly/{year}/{month}
```

Наприклад:

```text
GET /api/weather/monthly/2026/1
```

Приклад відповіді:

```json
{
  "average_temperature": -7.661290322580644,
  "precipitation_days": [1, 3, 7, 12, 18, 25]
}
```

`precipitation_days` містить номери днів місяця, коли кількість опадів була більшою за `0`.

---

# Redis Cache

Для кешування результатів аналітичних запитів використовується Redis.

Кешуються:

```text
weather:average:{start_date}:{end_date}
weather:extremes
weather:monthly:{year}:{month}
```

Час життя кешу:

```text
3600 секунд
```

Тобто результати важких повторних запитів можуть бути отримані з Redis без повторного виконання SQL-запиту до PostgreSQL.

Наприклад:

```text
weather:average:2026-01-01:2026-01-31
```

---

# PostgreSQL

Основна таблиця:

```text
weather
```

Має такі поля:

| Поле              | Тип     | Опис                    |
| ----------------- | ------- | ----------------------- |
| `id`              | Integer | Primary Key             |
| `date`            | Date    | Дата                    |
| `temperature_avg` | Float   | Середня температура     |
| `temperature_min` | Float   | Мінімальна температура  |
| `temperature_max` | Float   | Максимальна температура |
| `precipitation`   | Float   | Кількість опадів        |

Для `date` встановлено `UNIQUE` constraint, тому одна дата не може бути записана декілька разів.

---

# Тестування

Для запуску тестів:

```bash
pytest
```

Поточний результат:

```text
11 passed, 1 warning
```

Тести перевіряють:

* repository;
* analytics repository;
* service;
* API endpoints;
* валідацію параметрів;
* edge cases;
* роботу з Redis через mock/fake Redis;
* роботу з тестовою SQLite базою.

Попередження від `httpx` / Starlette не впливає на результат тестів.

---

# Валідація

API перевіряє некоректні параметри.

Наприклад, якщо:

```text
start_date > end_date
```

API повертає:

```http
400 Bad Request
```

з повідомленням:

```json
{
  "detail": "start_date must be before or equal to end_date"
}
```

Для некоректного місяця:

```text
/api/weather/monthly/2026/13
```

повертається:

```http
400 Bad Request
```

Для неправильного типу параметра FastAPI автоматично повертає:

```http
422 Unprocessable Entity
```

---

# Джерело даних

Історичні дані отримуються з:

**Open-Meteo Archive API**

API не потребує API key для цього сценарію.

Використовуються такі погодні показники:

* середня температура;
* мінімальна температура;
* максимальна температура;
* кількість опадів.

---

# Docker

Docker Compose автоматично запускає:

```text
FastAPI
   │
   ├── PostgreSQL
   │
   └── Redis
```

PostgreSQL та Redis мають health checks, тому API залежить від готовності цих сервісів.

Дані PostgreSQL та Redis зберігаються у Docker volumes:

```text
postgres_data
redis_data
```

Це дозволяє зберігати дані після перезапуску контейнерів.

---

# Перевірка роботи

Після запуску Docker можна перевірити:

### API

```bash
curl http://localhost:8000/docs
```

### PostgreSQL

```bash
docker compose exec db pg_isready -U weather_user -d weather_db
```

### Redis

```bash
docker compose exec cache redis-cli ping
```

Очікувана відповідь Redis:

```text
PONG
```

