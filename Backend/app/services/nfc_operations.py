from typing import Optional

from app.models.user import User


class NFCUserNotFoundError(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__("The requested user does not exist.")


class NFCAlreadyAssignedError(Exception):
    def __init__(self, existing_user: User):
        self.existing_user = existing_user
        super().__init__("The NFC card is already assigned.")


def ensure_nfc_available(
    existing_user: Optional[User],
    target_user_id: int,
) -> None:
    if existing_user is not None and existing_user.id != target_user_id:
        raise NFCAlreadyAssignedError(existing_user)


def require_user(user: Optional[User], identifier: str) -> User:
    if user is None:
        raise NFCUserNotFoundError(identifier)
    return user


def assign_nfc(user: User, nfc_uid: str) -> None:
    user.nfc_uid = nfc_uid


def unbind_nfc(user: User) -> None:
    user.nfc_uid = None
