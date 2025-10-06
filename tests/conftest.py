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
    from src.db.postgresql import get_db

    def _override():
        yield db

    fastapi_app.dependency_overrides[get_db] = _override
    yield
    fastapi_app.dependency_overrides.clear()
