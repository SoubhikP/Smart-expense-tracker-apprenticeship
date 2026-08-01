"""
Tests for the Expense Tracker API.

We use FastAPI's TestClient (built on `requests`-style calls) so we don't
need to actually start a server - it calls the app directly in memory,
which makes tests fast and reliable.

Run with:  pytest
"""

import pytest
from fastapi.testclient import TestClient

from src import storage
from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    """Runs before every single test so tests don't affect each other."""
    storage.clear_all()
    yield
    storage.clear_all()


def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200


def test_add_expense_success():
    response = client.post(
        "/expenses",
        json={"title": "Groceries", "amount": 45.50, "category": "Food", "date": "2026-01-15"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Groceries"
    assert data["amount"] == 45.50
    assert data["category"] == "Food"
    assert data["id"] == 1  # first expense should get id 1


def test_add_expense_rejects_negative_amount():
    # amount must be > 0, so this should fail validation with a 422 error
    response = client.post(
        "/expenses",
        json={"title": "Bad expense", "amount": -10, "category": "Food", "date": "2026-01-15"},
    )
    assert response.status_code == 422


def test_add_expense_rejects_missing_fields():
    response = client.post("/expenses", json={"title": "Missing stuff"})
    assert response.status_code == 422


def test_get_all_expenses():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"})
    client.post("/expenses", json={"title": "Bus ticket", "amount": 2.5, "category": "Travel", "date": "2026-01-02"})

    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_filter_expenses_by_category():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"})
    client.post("/expenses", json={"title": "Bus ticket", "amount": 2.5, "category": "Travel", "date": "2026-01-02"})
    client.post("/expenses", json={"title": "Pizza", "amount": 12, "category": "food", "date": "2026-01-03"})

    response = client.get("/expenses", params={"category": "Food"})
    assert response.status_code == 200
    data = response.json()
    # Filter should be case-insensitive, so this should catch both
    # "Food" and "food" entries -> 2 results.
    assert len(data) == 2
    assert all(e["category"].lower() == "food" for e in data)


def test_filter_by_nonexistent_category_returns_empty_list():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"})
    response = client.get("/expenses", params={"category": "Rent"})
    assert response.status_code == 200
    assert response.json() == []


def test_total_overall_and_by_category():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"})
    client.post("/expenses", json={"title": "Pizza", "amount": 15, "category": "Food", "date": "2026-01-02"})
    client.post("/expenses", json={"title": "Bus ticket", "amount": 2.5, "category": "Travel", "date": "2026-01-03"})

    response = client.get("/expenses/total")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_total"] == 22.5
    assert data["by_category"]["Food"] == 20
    assert data["by_category"]["Travel"] == 2.5


def test_total_for_specific_category():
    client.post("/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"})
    client.post("/expenses", json={"title": "Pizza", "amount": 15, "category": "Food", "date": "2026-01-02"})

    response = client.get("/expenses/total", params={"category": "Food"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 20


def test_delete_expense_success():
    add_response = client.post(
        "/expenses", json={"title": "Coffee", "amount": 5, "category": "Food", "date": "2026-01-01"}
    )
    expense_id = add_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 200

    get_response = client.get("/expenses")
    assert get_response.json() == []


def test_delete_nonexistent_expense_returns_404():
    response = client.delete("/expenses/9999")
    assert response.status_code == 404
