from faker import Faker
from src.api.users.schemas import CreateUserSchema
from src.api.common.schemas import CreateIngredientSchema
from src.api.common.schemas import CreateCategorySchema
from src.api.recipes.schemas import CreateRecipeSchema
from src.api.recipes.enums import DifficultyLevel

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


def make_ingredient_payload(
    *,
    categories_ids: list[int] | None = None,
    categories_names: list[str] | None = None,
    **overrides,
) -> CreateIngredientSchema:
    if categories_ids is None:
        categories_ids = [1, 2]
    if categories_names is None:
        categories_names = ["Veggies", "Fruits"]
    category_payloads = [
        {"id": category_id, "name": category_name}
        for category_id, category_name in zip(
            categories_ids, categories_names, strict=True
        )
    ]
    data = {
        "name": fake.unique.name(),
        "is_vegan": False,
        "categories": category_payloads,
    }
    data.update(overrides)
    return CreateIngredientSchema(**data)


def make_category_payload() -> CreateCategorySchema:
    return CreateCategorySchema(
        name=fake.unique.name(),
    )


def make_recipe_payload(
    *,
    user_id: int,
    ingredient_ids: list[int],
    quantities: list[str] | None = None,
    **overrides,
) -> CreateRecipeSchema:
    if quantities is None:
        quantities = ["1 unit"] * len(ingredient_ids)
    ingredient_payloads = [
        {"ingredient_id": ingredient_id, "quantity": quantity}
        for ingredient_id, quantity in zip(ingredient_ids, quantities, strict=True)
    ]
    data = {
        "name": fake.unique.word(),
        "cooking_time": fake.random_int(min=5, max=120),
        "difficulty_level": DifficultyLevel.EASY,
        "portions": fake.random_int(min=1, max=8),
        "instructions": fake.sentence(),
        "ingredients": ingredient_payloads,
        "user_id": user_id,
    }
    data.update(overrides)
    return CreateRecipeSchema(**data)
