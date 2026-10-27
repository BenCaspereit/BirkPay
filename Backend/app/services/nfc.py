from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserResponse


class NFCService:

    @staticmethod
    def get_user_by_nfc(db: Session, nfc_uid: str) -> UserResponse:
        """
        searches for a user by their NFC UID and returns the user data.
        called when a user taps their NFC card at the checkout.
        """
        user = db.query(User).filter(User.nfc_uid == nfc_uid).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kein Benutzer mit der NFC-ID '{nfc_uid}' gefunden."
            )
            
        return UserResponse.model_validate(user)

    @staticmethod
    def assign_nfc_to_user(db: Session, user_id: int, new_nfc_uid: str) -> UserResponse:
        """
        assigns a new NFC UID to a user. This is typically used when issuing a new card or reassigning a card to a different user.
        checks if the NFC UID is already assigned to another user and raises an error if so.
        """

        # 1. check if the new NFC UID is already assigned to another user
        existing_nfc = db.query(User).filter(User.nfc_uid == new_nfc_uid, User.id != user_id).first()
        if existing_nfc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Die NFC-Karte '{new_nfc_uid}' ist bereits dem Benutzer '{existing_nfc.name}' (ID: {existing_nfc.id}) zugewiesen."
            )

        # 2. search for the user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Benutzer mit ID {user_id} nicht gefunden."
            )

        # 3. assign and save
        user.nfc_uid = new_nfc_uid
        db.commit()
        db.refresh(user)

        return UserResponse.model_validate(user)

    @staticmethod
    def unbind_nfc(db: Session, user_id: int) -> UserResponse:
        """
        removes the NFC UID from a user, effectively unbinding the card from the account.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Benutzer mit ID {user_id} nicht gefunden."
            )

        user.nfc_uid = None
        db.commit()
        db.refresh(user)

        return UserResponse.model_validate(user)