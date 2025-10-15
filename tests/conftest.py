from __future__ import annotations
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from alembic.config import Config
from alembic import command
from testcontainers.postgres import PostgresContainer

from main import app as fastapi_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture(scope="session")
def _pg_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer(
        image="postgres:17-alpine",
        username="test",
        password="test",
        dbname="app_test",
    ) as pg:
        yield pg


@pytest.fixture(scope="session")
def pg_url(_pg_container) -> str:
    return _pg_container.get_connection_url()


@pytest.fixture(scope="session")
def engine(pg_url: str):
    engine = create_engine(pg_url, pool_pre_ping=True, future=True)

    cfg = Config("./alembic.ini")
    cfg.set_main_option("sqlalchemy.url", pg_url)
    cfg.set_main_option("script_location", "alembic")

    command.upgrade(cfg, "head")

    return engine


@pytest.fixture(scope="session")
def session_factory(engine: Engine):
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=Session,
    )


@pytest.fixture()
def db(session_factory) -> Generator[Session, None, None]:
    """
    Per-test DB session wrapped in a transaction.
    Everything is rolled back after each test for isolation & speed.
    """
    connection = session_factory.kw["bind"].connect()
    trans = connection.begin()
    try:
        session: Session = session_factory(bind=connection)
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()


@pytest.fixture(autouse=True)
def override_get_db(db: Session):
    from src.core.dependencies import get_db as app_get_db

    def _override():
        yield db

    fastapi_app.dependency_overrides[app_get_db] = _override
    yield
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def user(db: Session):
    from src.db.models.users import User
    from src.core.security import hash_password
    from tests.factories import make_user_payload

    payload = make_user_payload()
    hashed_password = hash_password(payload.password)
    row = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        is_active=payload.is_active,
        hashed_password=hashed_password,
    )
    db.add(row)
    db.flush()
    return row


@pytest.fixture()
def user_factory(db):
    from src.db.models.users import User
    from src.core.security import hash_password
    from tests.factories import make_user_payload

    def _create(**overrides):
        payload = make_user_payload(**overrides)
        row = User(
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            is_active=payload.is_active,
            hashed_password=hash_password(payload.password),
        )
        db.add(row)
        db.flush()
        return row

    return _create


@pytest.fixture()
def ingredient(db: Session):
    from src.db.models.ingredients import Ingredient
    from tests.factories import make_ingredient_payload

    payload = make_ingredient_payload()

    row = Ingredient(name=payload.name, is_vegan=payload.is_vegan)
    db.add(row)
    db.flush()
    return row


@pytest.fixture()
def ingredient_factory(db):
    from src.db.models.ingredients import Ingredient
    from tests.factories import make_ingredient_payload

    def _create(**overrides):
        payload = make_ingredient_payload(**overrides)
        row = Ingredient(
            name=payload.name,
            is_vegan=payload.is_vegan,
        )
        db.add(row)
        db.flush()
        return row

    return _create


@pytest.fixture()
def category(db: Session):
    from src.db.models.categories import Category
    from tests.factories import make_category_payload

    payload = make_category_payload()
    row = Category(
        name=payload.name,
    )
    db.add(row)
    db.flush()
    return row


@pytest.fixture()
def category_factory(db):
    from src.db.models.categories import Category
    from tests.factories import make_category_payload

    def _create(**overrides):
        payload = make_category_payload(**overrides)
        row = Category(
            name=payload.name,
        )
        db.add(row)
        db.flush()
        return row

    return _create
