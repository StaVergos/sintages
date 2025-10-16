from faker import Faker
from src.api.users.schemas import CreateUserSchema
from src.api.ingredients.schemas import CreateIngredientSchema
from src.api.categories.schemas import CreateCategorySchema

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


def make_ingredient_payload() -> CreateIngredientSchema:
    return CreateIngredientSchema(
        name=fake.unique.name(),
        is_vegan=False,
        category_id=fake.random_int(min=1, max=10),
    )


def make_category_payload() -> CreateCategorySchema:
    return CreateCategorySchema(
        name=fake.unique.name(),
    )
