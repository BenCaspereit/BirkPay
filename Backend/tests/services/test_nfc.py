import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.nfc import NFCService


def test_get_user_by_nfc_returns_matching_user(
    db_session: Session,
    user_factory,
):
    user = user_factory(name="Ada Lovelace", nfc_uid="card-ada", balance_cents=900)

    result = NFCService.get_user_by_nfc(db_session, "card-ada")

    assert result.id == user.id
    assert result.name == "Ada Lovelace"
    assert result.balance_cents == 900


def test_get_user_by_nfc_raises_404_for_unknown_card(db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        NFCService.get_user_by_nfc(db_session, "unknown-card")

    assert exc_info.value.status_code == 404


def test_assign_nfc_to_user_persists_new_card(
    db_session: Session,
    user_factory,
):
    user = user_factory(name="Grace Hopper")

    result = NFCService.assign_nfc_to_user(db_session, user.id, "card-grace")

    assert result.id == user.id
    assert result.nfc_uid == "card-grace"
    assert db_session.query(User).filter(User.id == user.id).one().nfc_uid == "card-grace"


def test_assign_nfc_to_user_rejects_card_owned_by_another_user(
    db_session: Session,
    user_factory,
):
    user_factory(name="Existing owner", nfc_uid="occupied-card")
    target = user_factory(name="Target user")

    with pytest.raises(HTTPException) as exc_info:
        NFCService.assign_nfc_to_user(db_session, target.id, "occupied-card")

    assert exc_info.value.status_code == 400


def test_assign_nfc_to_user_raises_404_for_unknown_user(db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        NFCService.assign_nfc_to_user(db_session, 9999, "new-card")

    assert exc_info.value.status_code == 404
