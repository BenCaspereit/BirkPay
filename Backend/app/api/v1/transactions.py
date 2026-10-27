from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, RoleChecker
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.checkout import CheckoutRequest, CheckoutResponse, TransactionResponse
from app.services.checkout_integration import CheckoutService
from app.services.checkout_operations import InsufficientBalanceException

router = APIRouter(prefix="/transactions", tags=["Transactions & Checkout"])


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    # Optional im MVP: check if the current user is a cashier or admin
    current_cashier: User = Depends(RoleChecker(["cashier", "admin"]))
):
    """
    Checkout:
    1. Identifies the user via NFC UID and locks the database row (row locking).
    2. Checks the balance against the price of the items in the shopping cart.
    3. Deducts the amount and creates the transaction entry.
    """
    try:
        cashier_id = request.cashier_user_id or current_cashier.id
        return CheckoutService.process_checkout(
            db=db,
            nfc_uid=request.nfc_uid,
            items=request.items,
            cashier_id=cashier_id
        )
    except InsufficientBalanceException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "INSUFFICIENT_BALANCE",
                "message": "Nicht genügend Guthaben vorhanden.",
                "current_balance_cents": e.current_balance,
                "required_amount_cents": e.required_amount
            }
        )


@router.get("/user/{user_id}", response_model=List[TransactionResponse])
def get_user_transactions(
    user_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve the payment history/transactions for a specific user.
    """
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .limit(limit)
        .all()
    )
    return transactions