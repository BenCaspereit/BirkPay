from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, RoleChecker
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.nfc import NFCService

router = APIRouter(prefix="/users", tags=["Users & NFC"])


@router.get("/by-nfc/{nfc_uid}", response_model=UserResponse)
def get_user_by_nfc(nfc_uid: str, db: Session = Depends(get_db)):
    """
    Card Lookup: Returns the name and balance
    as soon as the card is held up to the NFC scanner.
    """
    return NFCService.get_user_by_nfc(db, nfc_uid)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin"]))
):
    """
    Creates a new user (student / teacher).
    """
    if user_in.nfc_uid:
        existing = db.query(User).filter(User.nfc_uid == user_in.nfc_uid).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Die NFC-UID '{user_in.nfc_uid}' ist bereits vergeben."
            )
            
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lists all users of the school (for admin interface).
    """
    return db.query(User).offset(skip).limit(limit).all()


@router.post("/{user_id}/deposit", response_model=UserResponse)
def deposit_funds(
    user_id: int,
    amount_cents: int = Query(..., gt=0, description="Betrag in Cents zum Aufladen (z.B. 1000 für 10,00 €)"),
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin", "cashier"]))
):
    """
    Deposits funds into a user's account.
    """
    user = db.query(User).filter(User.id == user_id).with_for_update().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Benutzer mit ID {user_id} nicht gefunden."
        )

    user.balance_cents += amount_cents

    # Deposits in transaction table for history
    tx = Transaction(
        school_id=user.school_id,
        user_id=user.id,
        amount_cents=amount_cents,
        type="DEPOSIT"
    )
    db.add(tx)
    
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/nfc", response_model=UserResponse)
def assign_nfc_card(
    user_id: int,
    nfc_uid: str = Query(..., description="Die neue NFC-UID"),
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin", "cashier"]))
):
    """
    Assigns a new NFC card to a user.
    """
    return NFCService.assign_nfc_to_user(db, user_id, nfc_uid)