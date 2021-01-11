from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import UUID4

from app.auth.service import get_jwt_user_active
from app.videos import service as videos_service
from app.videos.constants import ErrorCode

from . import service

router = APIRouter()


@router.post("/{video_id}/like", status_code=status.HTTP_201_CREATED)
async def like_video(video_id: UUID4, user=Depends(get_jwt_user_active)):
    video = await videos_service.get_by_id(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.VIDEO_NOT_FOUND,
        )

    liked = await service.like_video(video_id, user["id"])
    if not liked:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/{video_id}/like", status_code=status.HTTP_200_OK)
async def dislike_video(video_id: UUID4, user=Depends(get_jwt_user_active)):
    return await service.dislike_video(video_id, user["id"])
