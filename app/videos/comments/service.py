from pydantic import UUID4

from app.database import database, video_comments

from .models import Comment


async def add_comment(comment: Comment):
    insert_query = (video_comments.insert().values(**comment.dict())).returning(
        video_comments
    )

    return await database.fetch_one(insert_query)


async def delete_comment(comment_id: UUID4):
    delete_query = video_comments.delete().where(video_comments.c.id == comment_id)

    return await database.execute(delete_query)


async def is_owner(comment_id: UUID4, user_id: UUID4):
    delete_query = video_comments.select().where(
        (video_comments.c.id == comment_id) & (video_comments.c.user_id == user_id)
    )

    return await database.fetch_one(delete_query)
