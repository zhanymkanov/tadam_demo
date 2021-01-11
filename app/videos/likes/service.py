import uuid

from asyncpg.exceptions import UniqueViolationError
from pydantic import UUID4

from app.database import database, video_likes


async def like_video(video_id: UUID4, user_id: UUID4):
    insert_query = (
        video_likes.insert().values(id=uuid.uuid4(), video_id=video_id, user_id=user_id)
    ).returning(video_likes.c.id)
    try:
        return await database.execute(insert_query)
    except UniqueViolationError:
        return


async def dislike_video(video_id: UUID4, user_id: UUID4):
    delete_query = video_likes.delete().where(
        (video_likes.c.video_id == video_id) & (video_likes.c.user_id == user_id)
    )

    return await database.execute(delete_query)
