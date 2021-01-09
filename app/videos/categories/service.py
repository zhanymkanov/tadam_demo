from typing import List, Optional

from sqlalchemy import select

from app.database import categories, database, users, videos
from app.videos.models import VideoResponse

from .models import Category


async def get_by_slug(category_slug: str) -> Optional[Category]:
    select_query = categories.select().where(categories.c.slug == category_slug)

    category = await database.fetch_one(select_query)
    if not category:
        return

    return category


async def create(category: Category) -> Category:
    insert_query = categories.insert().values(**category.dict()).returning(categories)

    category_created = await database.fetch_one(insert_query)
    return category_created


async def get_category_videos(category_slug: str) -> List[VideoResponse]:
    category = videos.join(categories).join(users)
    extract_query = (
        select(
            [
                videos,
                categories.c.title.label("category"),
                categories.c.slug.label("category_slug"),
                users.c.email.label("owner"),
            ]
        )
        .select_from(category)
        .where(categories.c.slug == category_slug)
    )
    stored_video = await database.fetch_all(extract_query)

    return stored_video
