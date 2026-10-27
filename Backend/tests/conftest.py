import os
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.api.deps import get_db
from app.db.session import Base
from app.main import app
from app.models.product import Product
from app.models.user import User


@pytest.fixture
def engine():
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    try:
        yield test_engine
    finally:
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture
def db_session(engine) -> Session:
    test_session_maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    db = test_session_maker()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session: Session):
    def override_get_db():
        yield db_session

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)


@pytest.fixture
def user_factory(db_session: Session) -> Callable[..., User]:
    def create_user(
        *,
        name: str = "Test User",
        nfc_uid: str | None = None,
        balance_cents: int = 0,
        role: str = "student",
        school_id: str = "schule-1",
    ) -> User:
        user = User(
            name=name,
            nfc_uid=nfc_uid,
            balance_cents=balance_cents,
            role=role,
            school_id=school_id,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return create_user


@pytest.fixture
def product_factory(db_session: Session) -> Callable[..., Product]:
    def create_product(
        *,
        name: str = "Test Product",
        price_cents: int = 150,
        is_active: bool = True,
        school_id: str = "schule-1",
    ) -> Product:
        product = Product(
            name=name,
            price_cents=price_cents,
            is_active=is_active,
            school_id=school_id,
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        return product

    return create_product


@pytest.fixture
def role_headers(user_factory: Callable[..., User]) -> Callable[[str], dict[str, str]]:
    def headers_for_role(role: str) -> dict[str, str]:
        user = user_factory(
            name=f"Test {role}",
            role=role,
            nfc_uid=f"test-{role}-card",
        )
        return {"X-NFC-Key": user.nfc_uid}

    return headers_for_role
