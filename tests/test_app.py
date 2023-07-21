import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from event_service.models.database import Base
from event_service.main import app
from event_service.dependencies import get_db, get_current_user
from event_service.auth.app_dependencies import oauth2_scheme



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


def override_get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    else:
        return "tester"


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_user

test_client = TestClient(app)


def test_401_when_no_bearer_token():
    response = test_client.get("/events")
    assert response.status_code == 401


def test_auth_no_data():
    response = test_client.post("/auth")
    assert response.status_code == 422


def test_auth_correct_data():
    response = test_client.post("/auth",
                                data={"username": "tester",
                                      "password": "secret",
                                      "grant_type": "password"
                                      }
                                )
    assert response.status_code == 200


def test_create_events():
    response = test_client.post(
        "/events/",
        json={"name": "test1"},
        headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'test1'


def test_get_events():
    response = test_client.get("/events", headers={"Authorization": "Bearer testtoken"})
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
    response = test_client.get("/events/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['id'] == 1
    assert data['name'] == 'test1'

