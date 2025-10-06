import pytest
from src.db.models.users import User
from tests.factories import make_user_payload
from fastapi.testclient import TestClient


@pytest.mark.anyio
def test_create_user(client: TestClient):
    payload = make_user_payload()
    resp = client.post("/users", json=payload.model_dump())
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == payload.email
    assert data["full_name"] == payload.full_name
    assert "id" in data


@pytest.mark.anyio
def test_get_user(client: TestClient, user: User):
    resp = client.get(f"/users/{user.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user.id
    assert data["username"] == user.username
    assert data["email"] == user.email


@pytest.mark.anyio
def test_list_users(client: TestClient, user_factory: callable):
    u1 = user_factory()
    u2 = user_factory()
    resp = client.get("/users")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    ids = {u["id"] for u in resp.json()}
    assert ids == {u1.id, u2.id}
