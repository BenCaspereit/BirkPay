from typing import Generator
from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
    """
    starts a new database session for each request
    and closes it after the request is completed. 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_by_nfc(
    x_nfc_key: str = Header(..., description="NFC-UID der Kasse / des Users zur Authentifizierung"),
    db: Session = Depends(get_db)
) -> User:
    """
    Security dependency for the MVP:
    Reads the NFC UID from the ‘X-NFC-Key’ header and loads the corresponding user.
    """
    user = db.query(User).filter(User.nfc_uid == x_nfc_key).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Authentifizierung (NFC-Key nicht gefunden)."
        )
    return user


class RoleChecker:
    """
    Checks if the calling user has the required role.
    Example for routes: Depends(RoleChecker(["cashier", "admin"]))
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user_by_nfc)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Zugriff verweigert. Erforderliche Rolle: {self.allowed_roles}"
            )
        return current_user