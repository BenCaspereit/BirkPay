from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User


def test_create_user_lookup_nfc_and_deposit_happy_path(
    client,
    db_session: Session,
    role_headers,
):
    admin_headers = role_headers("admin")
    response = client.post(
        "/api/v1/users/",
        headers=admin_headers,
        json={
            "name": "New Student",
            "nfc_uid": "new-student-card",
            "balance_cents": 250,
        },
    )

    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == "New Student"
    assert created_user["balance_cents"] == 250

    lookup = client.get("/api/v1/users/by-nfc/new-student-card")
    assert lookup.status_code == 200
    assert lookup.json()["id"] == created_user["id"]

    deposit = client.post(
        f"/api/v1/users/{created_user['id']}/deposit",
        headers=admin_headers,
        params={"amount_cents": 500},
    )
    assert deposit.status_code == 200
    assert deposit.json()["balance_cents"] == 750

    transaction = db_session.query(Transaction).filter(
        Transaction.user_id == created_user["id"]
    ).one()
    assert transaction.amount_cents == 500
    assert transaction.type == "DEPOSIT"


def test_create_user_rejects_duplicate_nfc_uid(client, role_headers, user_factory):
    user_factory(name="Existing", nfc_uid="taken-card")

    response = client.post(
        "/api/v1/users/",
        headers=role_headers("admin"),
        json={"name": "Duplicate", "nfc_uid": "taken-card"},
    )

    assert response.status_code == 400


def test_non_admin_cannot_create_user(client, role_headers):
    response = client.post(
        "/api/v1/users/",
        headers=role_headers("cashier"),
        json={"name": "Unauthorized", "nfc_uid": "unauthorized-card"},
    )

    assert response.status_code == 403


def test_deposit_returns_404_for_unknown_user(client, role_headers):
    response = client.post(
        "/api/v1/users/9999/deposit",
        headers=role_headers("cashier"),
        params={"amount_cents": 100},
    )

    assert response.status_code == 404


def test_nfc_lookup_returns_404_for_unknown_card(client):
    response = client.get("/api/v1/users/by-nfc/unknown-card")

    assert response.status_code == 404


def test_assign_nfc_returns_400_for_already_assigned_card(
    client,
    role_headers,
    user_factory,
):
    user_factory(name="Existing", nfc_uid="occupied-card")
    target = user_factory(name="Target")

    response = client.put(
        f"/api/v1/users/{target.id}/nfc",
        headers=role_headers("admin"),
        params={"nfc_uid": "occupied-card"},
    )

    assert response.status_code == 400


def test_assign_nfc_returns_404_for_unknown_user(client, role_headers):
    response = client.put(
        "/api/v1/users/9999/nfc",
        headers=role_headers("admin"),
        params={"nfc_uid": "new-card"},
    )

    assert response.status_code == 404
