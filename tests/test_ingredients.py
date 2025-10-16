import pytest
from src.db.models.ingredients import Ingredient
from tests.factories import make_ingredient_payload
from fastapi.testclient import TestClient


@pytest.mark.anyio
def test_create_ingredient(client: TestClient):
    payload = make_ingredient_payload()
    resp = client.post("/ingredients", json=payload.model_dump())
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == payload.name
    assert "id" in data


@pytest.mark.anyio
def test_get_ingredient(client: TestClient, ingredient: Ingredient):
    resp = client.get(f"/ingredients/{ingredient.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == ingredient.id
    assert data["name"] == ingredient.name
    assert data["category_id"] == ingredient.category_id


@pytest.mark.anyio
def test_list_ingredients(client: TestClient, ingredient_factory: callable):
    i1 = ingredient_factory()
    i2 = ingredient_factory()
    resp = client.get("/ingredients")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    ids = {i["id"] for i in resp.json()}
    assert ids == {i1.id, i2.id}


@pytest.mark.anyio
def test_update_ingredient(client: TestClient, ingredient: Ingredient):
    new_payload = make_ingredient_payload()
    resp = client.put(f"/ingredients/{ingredient.id}", json=new_payload.model_dump())
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == ingredient.id
    assert data["name"] == new_payload.name
    assert data["is_vegan"] == new_payload.is_vegan
    assert data["category_id"] == new_payload.category_id
