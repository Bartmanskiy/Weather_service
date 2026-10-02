import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.db.database import Base, get_db
from app.main import app
from app.cache.redis import get_redis


TEST_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class FakeRedis:

    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, ex=None):
        self.data[key] = value

    def ping(self):
        return True

    def flushall(self):
        self.data.clear()

    def keys(self, pattern):
        if pattern == "weather:*":
            return [
                key
                for key in self.data
                if key.startswith("weather:")
            ]

        return []

    def delete(self, *keys):
        for key in keys:
            self.data.pop(key, None)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def client(db_session, fake_redis):
    def override_get_db():
        yield db_session

    def override_get_redis():
        return fake_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    yield TestClient(app)

    app.dependency_overrides.clear()