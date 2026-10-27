from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.product import Product
from app.models.transaction import Transaction
from app.schemas.checkout import CartItem, CheckoutResponse


class InsufficientBalanceException(Exception):
    """is raised when a user tries to checkout with insufficient balance."""
    def __init__(self, current_balance: int, required_amount: int):
        self.current_balance = current_balance
        self.required_amount = required_amount
        super().__init__(f"Guthaben nicht ausreichend. Vorhanden: {current_balance} Cents, Benötigt: {required_amount} Cents")


class CheckoutService:
    
    @staticmethod
    def process_checkout(
        db: Session, 
        nfc_uid: str, 
        items: List[CartItem], 
        cashier_id: int = None
    ) -> CheckoutResponse:
        """
        Performs the checkout process atomically:
        1. Locks the user row in the database (row locking) to prevent concurrent access.
        2. Calculates the total price based on the current product prices.
        3. Checks whether the account balance is sufficient.
        4. Deducts the amount and creates the transaction entry.
        5. Executes the database commit.
        """
        
        # 1. search for the user by NFC UID and lock the row for update
        user = (
            db.query(User)
            .filter(User.nfc_uid == nfc_uid)
            .with_for_update()  # blocks the row to prevent concurrent modifications
            .first()
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kein Benutzer mit der NFC-ID '{nfc_uid}' gefunden."
            )

        # 2. calculate total price based on current product prices
        product_ids = [item.product_id for item in items]
        products = db.query(Product).filter(Product.id.in_(product_ids), Product.is_active == True).all()
        product_map = {p.id: p for p in products}

        total_price_cents = 0
        for item in items:
            product = product_map.get(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Produkt mit ID {item.product_id} ist ungültig oder inaktiv."
                )
            total_price_cents += product.price_cents * item.quantity

        if total_price_cents <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Der Gesamtbetrag des Warenkorbs muss größer als 0 Cents sein."
            )

        # 3. balance check
        if user.balance_cents < total_price_cents:
            raise InsufficientBalanceException(
                current_balance=user.balance_cents, 
                required_amount=total_price_cents
            )

        # 4. Create a Debit & Transaction
        user.balance_cents -= total_price_cents

        new_transaction = Transaction(
            school_id=user.school_id,
            user_id=user.id,
            amount_cents=-total_price_cents,  # negative because it's a debit
            type="PURCHASE",
            created_by_user_id=cashier_id
        )

        db.add(new_transaction)
        
        # 5. save changes to the database
        db.commit()
        db.refresh(user)
        db.refresh(new_transaction)

        return CheckoutResponse(
            success=True,
            transaction_id=new_transaction.id,
            user_id=user.id,
            user_name=user.name,
            total_amount_cents=total_price_cents,
            new_balance_cents=user.balance_cents,
            timestamp=new_transaction.created_at
        )