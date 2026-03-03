import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Home & Health ─────────────────────────────────────────────────────────────

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "running"
    assert "message" in data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


# ── GET /items ────────────────────────────────────────────────────────────────

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert "count" in data
    assert isinstance(data["items"], list)


def test_get_item_by_id(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1


def test_get_item_not_found(client):
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


# ── POST /items ───────────────────────────────────────────────────────────────

def test_create_item(client):
    payload = {"name": "Test Item", "description": "Created in test"}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Item"
    assert "id" in data


def test_create_item_missing_name(client):
    response = client.post("/items", json={"description": "no name"})
    assert response.status_code == 400
    assert "error" in response.get_json()


# ── DELETE /items ─────────────────────────────────────────────────────────────

def test_delete_item(client):
    response = client.delete("/items/2")
    assert response.status_code == 200
    assert "deleted" in response.get_json()["message"]


def test_delete_item_not_found(client):
    response = client.delete("/items/9999")
    assert response.status_code == 404
