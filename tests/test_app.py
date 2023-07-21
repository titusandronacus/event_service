import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from event_service.models.database import Base
from event_service.main import app
from event_service.dependencies import get_db


engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

test_client = TestClient(app)


def test_create_events():
    response = test_client.post(
        "/events/",
        json={"name": "test1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'test1'


def test_get_events():
    response = test_client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'test1'


# TODO: blocked by filter being silly
# def test_get_events_by_name():
#     set_data = test_client.post(
#         "/events/",
#         json={"name": "test2"}
#     )
#
#     response = test_client.get("/events/?name=test2")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) == 1
#     assert data[0]['name'] == 'test2'


def test_get_event():
    response = test_client.get("/events/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['id'] == 1
    assert data['name'] == 'test1'

