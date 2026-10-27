from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User


def test_checkout_endpoint_charges_user_and_returns_receipt(
    client,
    db_session: Session,
    role_headers,
    user_factory,
    product_factory,
):
    buyer = user_factory(name="Buyer", nfc_uid="buyer-card", balance_cents=1000)
    cashier_headers = role_headers("cashier")
    product_factory(name="Sandwich", price_cents=325)

    response = client.post(
        "/api/v1/transactions/checkout",
        headers=cashier_headers,
        json={
            "nfc_uid": "buyer-card",
            "items": [{"product_id": 1, "quantity": 2}],
        },
    )

    assert response.status_code == 200
    receipt = response.json()
    assert receipt["success"] is True
    assert receipt["user_id"] == buyer.id
    assert receipt["total_amount_cents"] == 650
    assert receipt["new_balance_cents"] == 350

    persisted_buyer = db_session.query(User).filter(User.id == buyer.id).one()
    assert persisted_buyer.balance_cents == 350
    transaction = db_session.query(Transaction).one()
    assert transaction.amount_cents == -650
    assert transaction.type == "PURCHASE"


def test_checkout_endpoint_returns_400_when_balance_is_insufficient(
    client,
    role_headers,
    user_factory,
    product_factory,
):
    user_factory(nfc_uid="buyer-card", balance_cents=100)
    product_factory(price_cents=250)

    response = client.post(
        "/api/v1/transactions/checkout",
        headers=role_headers("cashier"),
        json={
            "nfc_uid": "buyer-card",
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "INSUFFICIENT_BALANCE"
    assert response.json()["detail"]["current_balance_cents"] == 100
    assert response.json()["detail"]["required_amount_cents"] == 250


def test_checkout_endpoint_rejects_unknown_or_inactive_product(
    client,
    role_headers,
    user_factory,
    product_factory,
):
    user_factory(nfc_uid="buyer-card", balance_cents=1000)
    product_factory(is_active=False)

    response = client.post(
        "/api/v1/transactions/checkout",
        headers=role_headers("cashier"),
        json={
            "nfc_uid": "buyer-card",
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )

    assert response.status_code == 400


def test_checkout_endpoint_rejects_non_cashier_role(
    client,
    role_headers,
    user_factory,
    product_factory,
):
    user_factory(nfc_uid="buyer-card", balance_cents=1000)
    product_factory()

    response = client.post(
        "/api/v1/transactions/checkout",
        headers=role_headers("student"),
        json={
            "nfc_uid": "buyer-card",
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )

    assert response.status_code == 403
