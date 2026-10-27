from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserResponse
from app.services.nfc_operations import (
    NFCAlreadyAssignedError,
    NFCUserNotFoundError,
    assign_nfc,
    ensure_nfc_available,
    require_user,
    unbind_nfc,
)


class NFCIntegrationService:
    @staticmethod
    def get_user_by_nfc(db: Session, nfc_uid: str) -> UserResponse:
        user = db.query(User).filter(User.nfc_uid == nfc_uid).first()

        try:
            user = require_user(user, nfc_uid)
        except NFCUserNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kein Benutzer mit der NFC-ID '{error.identifier}' gefunden.",
            ) from error

        return UserResponse.model_validate(user)

    @staticmethod
    def assign_nfc_to_user(
        db: Session,
        user_id: int,
        new_nfc_uid: str,
    ) -> UserResponse:
        existing_user = (
            db.query(User)
            .filter(User.nfc_uid == new_nfc_uid, User.id != user_id)
            .first()
        )
        try:
            ensure_nfc_available(existing_user, user_id)
        except NFCAlreadyAssignedError as error:
            existing = error.existing_user
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Die NFC-Karte '{new_nfc_uid}' ist bereits dem Benutzer "
                    f"'{existing.name}' (ID: {existing.id}) zugewiesen."
                ),
            ) from error

        user = db.query(User).filter(User.id == user_id).first()
        try:
            user = require_user(user, str(user_id))
        except NFCUserNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Benutzer mit ID {error.identifier} nicht gefunden.",
            ) from error

        assign_nfc(user, new_nfc_uid)
        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user)

    @staticmethod
    def unbind_nfc(db: Session, user_id: int) -> UserResponse:
        user = db.query(User).filter(User.id == user_id).first()
        try:
            user = require_user(user, str(user_id))
        except NFCUserNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Benutzer mit ID {error.identifier} nicht gefunden.",
            ) from error

        unbind_nfc(user)
        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user)
