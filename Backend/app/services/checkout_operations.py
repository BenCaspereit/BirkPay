from collections.abc import Mapping, Sequence

from fastapi import HTTPException, status

from app.schemas.checkout import CartItem


class InsufficientBalanceException(Exception):
    def __init__(self, current_balance: int, required_amount: int):
        self.current_balance = current_balance
        self.required_amount = required_amount
        super().__init__(
            f"Guthaben nicht ausreichend. Vorhanden: {current_balance} Cents, "
            f"Benötigt: {required_amount} Cents"
        )


def calculate_total(
    items: Sequence[CartItem],
    product_prices: Mapping[int, int],
) -> int:
    total_price_cents = 0

    for item in items:
        price_cents = product_prices.get(item.product_id)
        if price_cents is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produkt mit ID {item.product_id} ist ungültig oder inaktiv.",
            )
        total_price_cents += price_cents * item.quantity

    if total_price_cents <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Der Gesamtbetrag des Warenkorbs muss größer als 0 Cents sein.",
        )

    return total_price_cents


def ensure_sufficient_balance(current_balance: int, required_amount: int) -> None:
    if current_balance < required_amount:
        raise InsufficientBalanceException(current_balance, required_amount)
