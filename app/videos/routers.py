from typing import Optional, Tuple

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import UUID4

from app.auth.service import get_jwt_user_active
from app.videos import service
from app.videos.models import VideoResponse, VideoUpload
from app.videos.tags import service as tags_service
from app.videos.tags.models import Tag
from app.videos.tags.utils import clean_tags

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=VideoResponse)
async def post_video(
    title: str = Form(...),
    description: str = Form(...),
    category_id: UUID4 = Form(...),
    tags: Optional[Tuple[Tag]] = Depends(clean_tags),
    video_file: UploadFile = File(...),
    user=Depends(get_jwt_user_active),
):
    file_path = await service.save_video(video_file)
    video_stored = await service.create(
        VideoUpload(
            title=title,
            description=description,
            owner_id=user["id"],
            category_id=category_id,
            file_path=file_path,
        )
    )
    if tags:
        stored_tags = await tags_service.add_video_tags(video_stored.id, tags)
        video_stored.tags = stored_tags

    return video_stored


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: UUID4):
    return await service.get_joined_by_id(video_id)


@router.get("/{video_id}/stream", response_model=VideoResponse)
async def stream_video(video_id: UUID4):
    video_stored = await service.get_joined_by_id(video_id)
    return StreamingResponse(await service.stream_file(video_stored.file_path))
