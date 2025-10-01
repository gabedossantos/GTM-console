"""Integration tests for JourneyLens backend endpoints."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

AUTH_HEADERS = {"Authorization": "Bearer demo-token"}


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_list_accounts(client: TestClient) -> None:
    response = client.get("/accounts", headers=AUTH_HEADERS)
    assert response.status_code == 200
    accounts = response.json()
    assert isinstance(accounts, list)
    assert len(accounts) >= 1
    assert {"id", "name", "industry"}.issubset(accounts[0].keys())


def test_create_interaction_generates_insight(client: TestClient) -> None:
    payload = {
        "account_id": 1,
        "channel": "email",
        "content": "Customer is considering cancellation due to integration issues.",
    }
    response = client.post("/interactions", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 201
    insight = response.json()
    assert insight["intent"] in {"support_request", "churn_risk", "pricing_inquiry"}
    assert 0 <= insight["risk_score"] <= 1


def test_rag_answers_query(client: TestClient) -> None:
    response = client.get(
        "/accounts/1/rag",
        params={"query": "What is the current customer intent?"},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["account_id"] == 1