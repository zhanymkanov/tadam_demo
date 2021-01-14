from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4

from app.auth.service import get_jwt_user_active

from . import service
from .constants import ErrorCode
from .models import Comment
from .utils import comment_with_user

router = APIRouter()


@router.post("/{video_id}/comments", status_code=status.HTTP_201_CREATED)
async def comment_video(comment: Comment = Depends(comment_with_user)):
    return await service.add_comment(comment)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: UUID4, user=Depends(get_jwt_user_active)):
    if not await service.is_owner(comment_id, user["id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=ErrorCode.USER_NOT_OWNER
        )

    return await service.delete_comment(comment_id)


@router.patch("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def edit_comment(comment_id: UUID4, user=Depends(get_jwt_user_active)):
    pass
