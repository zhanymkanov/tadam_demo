import uuid
from typing import Mapping, Tuple

from pydantic import UUID4
from sqlalchemy.dialects.postgresql import insert

from app.database import database
from app.database import tags as tags_table
from app.database import video_tags
from app.utils import pydantic_to_dict

from .constants import VIDEO_TAG_UNIQUE_CONSTRAINT
from .models import Tag


async def add_video_tags(video_id: UUID4, tags: Tuple[Tag]):
    await create_multiple(tags)
    stored_tags = await get_by_title(tags)

    await _add_m2m_video_tags(video_id, stored_tags)

    return stored_tags


async def create_multiple(tags: Tuple[Tag]):
    insert_query = (
        insert(tags_table)
        .values(pydantic_to_dict(tags))
        .on_conflict_do_nothing(index_elements=["title"])
    )

    return await database.execute(insert_query)


async def get_by_title(tags: Tuple[Tag]):
    tags_titles = tuple(tag.title for tag in tags)
    select_query = tags_table.select().where(tags_table.c.title.in_(tags_titles))

    return await database.fetch_all(select_query)


async def _add_m2m_video_tags(video_id: UUID4, tags: Tuple[Mapping]):
    video_tag_ids = [
        {"video_id": video_id, "tag_id": tag["id"], "id": uuid.uuid4()} for tag in tags
    ]

    insert_query = (
        insert(video_tags)
        .values(video_tag_ids)
        .on_conflict_do_nothing(constraint=VIDEO_TAG_UNIQUE_CONSTRAINT)
    )

    return await database.execute(insert_query)
