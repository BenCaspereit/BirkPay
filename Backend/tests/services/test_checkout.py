import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.checkout import CartItem
from app.services.checkout_integration import CheckoutService
from app.services.checkout_operations import InsufficientBalanceException


def test_process_checkout_debits_balance_and_records_transaction(
    db_session: Session,
    user_factory,
    product_factory,
):
    buyer = user_factory(nfc_uid="buyer-card", balance_cents=1000)
    cashier = user_factory(nfc_uid="cashier-card", role="cashier")
    product_factory(name="Juice", price_cents=175)

    result = CheckoutService.process_checkout(
        db_session,
        nfc_uid="buyer-card",
        items=[CartItem(product_id=1, quantity=2)],
        cashier_id=cashier.id,
    )

    assert result.success is True
    assert result.total_amount_cents == 350
    assert result.new_balance_cents == 650
    assert db_session.query(User).filter(User.id == buyer.id).one().balance_cents == 650

    transaction = db_session.query(Transaction).one()
    assert transaction.user_id == buyer.id
    assert transaction.amount_cents == -350
    assert transaction.type == "PURCHASE"
    assert transaction.created_by_user_id == cashier.id


def test_process_checkout_raises_insufficient_balance_without_debit(
    db_session: Session,
    user_factory,
    product_factory,
):
    buyer = user_factory(nfc_uid="buyer-card", balance_cents=200)
    product_factory(price_cents=300)

    with pytest.raises(InsufficientBalanceException) as exc_info:
        CheckoutService.process_checkout(
            db_session,
            nfc_uid="buyer-card",
            items=[CartItem(product_id=1, quantity=1)],
        )

    assert exc_info.value.current_balance == 200
    assert exc_info.value.required_amount == 300
    assert db_session.query(User).filter(User.id == buyer.id).one().balance_cents == 200
    assert db_session.query(Transaction).count() == 0


def test_process_checkout_rejects_missing_or_inactive_product(
    db_session: Session,
    user_factory,
    product_factory,
):
    user_factory(nfc_uid="buyer-card", balance_cents=1000)
    product_factory(is_active=False)

    with pytest.raises(HTTPException) as exc_info:
        CheckoutService.process_checkout(
            db_session,
            nfc_uid="buyer-card",
            items=[CartItem(product_id=1, quantity=1)],
        )

    assert exc_info.value.status_code == 400
    assert db_session.query(Transaction).count() == 0


def test_process_checkout_raises_404_for_unknown_nfc(
    db_session: Session,
    product_factory,
):
    product_factory()

    with pytest.raises(HTTPException) as exc_info:
        CheckoutService.process_checkout(
            db_session,
            nfc_uid="unknown-card",
            items=[CartItem(product_id=1, quantity=1)],
        )

    assert exc_info.value.status_code == 404
