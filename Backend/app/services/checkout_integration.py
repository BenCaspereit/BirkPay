from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.checkout import CartItem, CheckoutResponse
from app.services.checkout_operations import (
    calculate_total,
    ensure_sufficient_balance,
)


class CheckoutService:
    @staticmethod
    def process_checkout(
        db: Session,
        nfc_uid: str,
        items: List[CartItem],
        cashier_id: Optional[int] = None,
    ) -> CheckoutResponse:
        user = CheckoutService._load_and_lock_user(db, nfc_uid)
        product_prices = CheckoutService._load_product_prices(db, items)
        total_price_cents = calculate_total(items, product_prices)
        ensure_sufficient_balance(user.balance_cents, total_price_cents)
        transaction = CheckoutService._debit_user(
            db, user, total_price_cents, cashier_id
        )
        CheckoutService._commit_and_refresh(db, user, transaction)
        return CheckoutService._build_response(user, transaction, total_price_cents)

    @staticmethod
    def _load_and_lock_user(db: Session, nfc_uid: str) -> User:
        user = (
            db.query(User)
            .filter(User.nfc_uid == nfc_uid)
            .with_for_update()
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kein Benutzer mit der NFC-ID '{nfc_uid}' gefunden.",
            )
        return user

    @staticmethod
    def _load_product_prices(db: Session, items: List[CartItem]) -> dict[int, int]:
        product_ids = [item.product_id for item in items]
        products = (
            db.query(Product)
            .filter(Product.id.in_(product_ids), Product.is_active == True)
            .all()
        )
        return {product.id: product.price_cents for product in products}

    @staticmethod
    def _debit_user(
        db: Session,
        user: User,
        total_price_cents: int,
        cashier_id: Optional[int],
    ) -> Transaction:
        user.balance_cents -= total_price_cents
        transaction = Transaction(
            school_id=user.school_id,
            user_id=user.id,
            amount_cents=-total_price_cents,
            type="PURCHASE",
            created_by_user_id=cashier_id,
        )
        db.add(transaction)
        return transaction

    @staticmethod
    def _commit_and_refresh(
        db: Session,
        user: User,
        transaction: Transaction,
    ) -> None:
        db.commit()
        db.refresh(user)
        db.refresh(transaction)

    @staticmethod
    def _build_response(
        user: User,
        transaction: Transaction,
        total_price_cents: int,
    ) -> CheckoutResponse:
        return CheckoutResponse(
            success=True,
            transaction_id=transaction.id,
            user_id=user.id,
            user_name=user.name,
            total_amount_cents=total_price_cents,
            new_balance_cents=user.balance_cents,
            timestamp=transaction.created_at,
        )
