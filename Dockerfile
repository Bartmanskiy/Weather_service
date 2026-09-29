FROM python:3.11-slim

# Створюємо окремого користувача
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Спочатку копіюємо тільки залежності
COPY requirements.txt .

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r requirements.txt

# Потім копіюємо код
COPY app ./app

# Передаємо права appuser
RUN chown -R appuser:appuser /app

# Не запускаємо контейнер від root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]