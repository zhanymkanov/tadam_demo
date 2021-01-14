from fastapi import Body, Depends
from pydantic import UUID4

from app.auth.service import get_jwt_user_active

from .models import Comment


async def comment_with_user(
    video_id: UUID4, text: str = Body(...), user=Depends(get_jwt_user_active)
):
    return Comment(video_id=video_id, user_id=user["id"], text=text)
