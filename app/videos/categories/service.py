from typing import Optional

from app.database import categories, database

from .models import Category


async def get_by_slug(category_slug: str) -> Optional[Category]:
    select_query = categories.select().where(categories.c.slug == category_slug)

    category = await database.fetch_one(select_query)
    if not category:
        return

    return Category(**category)


async def create(category: Category) -> Category:
    insert_query = categories.insert().values(**category.dict()).returning(categories)

    category = await database.fetch_one(insert_query)
    return Category(**category)
