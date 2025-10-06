from __future__ import annotations

from faker import Faker
from src.api.schemas import CreateUserSchema

fake = Faker()


def make_user_payload() -> CreateUserSchema:
    return CreateUserSchema(
        username=fake.unique.user_name(),
        email=fake.unique.email(),
        full_name=fake.name(),
        is_active=True,
        password=fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        ),
    )
