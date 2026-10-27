from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services.checkout_operations import (
    InsufficientBalanceException,
    calculate_total,
    ensure_sufficient_balance,
)


def test_calculate_total_sums_multiple_cart_items():
    items = [
        SimpleNamespace(product_id=1, quantity=2),
        SimpleNamespace(product_id=2, quantity=3),
    ]

    assert calculate_total(items, {1: 125, 2: 80}) == 490


def test_calculate_total_rejects_unknown_or_inactive_product():
    items = [SimpleNamespace(product_id=7, quantity=1)]

    with pytest.raises(HTTPException) as exc_info:
        calculate_total(items, {})

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Produkt mit ID 7 ist ungültig oder inaktiv."


def test_calculate_total_rejects_zero_total():
    items = [SimpleNamespace(product_id=1, quantity=1)]

    with pytest.raises(HTTPException) as exc_info:
        calculate_total(items, {1: 0})

    assert exc_info.value.status_code == 400
    assert (
        exc_info.value.detail
        == "Der Gesamtbetrag des Warenkorbs muss größer als 0 Cents sein."
    )


def test_ensure_sufficient_balance_accepts_sufficient_balance():
    ensure_sufficient_balance(current_balance=500, required_amount=500)


def test_ensure_sufficient_balance_raises_with_correct_amounts():
    with pytest.raises(InsufficientBalanceException) as exc_info:
        ensure_sufficient_balance(current_balance=200, required_amount=350)

    assert exc_info.value.current_balance == 200
    assert exc_info.value.required_amount == 350
