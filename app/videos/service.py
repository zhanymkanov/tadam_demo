from typing import Generator

from fastapi import UploadFile
from pydantic import UUID4
from sqlalchemy import select

from app.database import categories, database, users, videos
from app.videos.models import VideoResponse, VideoUpload
from app.videos.utils import generate_file_path, read_by_chunks


async def get_joined_by_id(video_id: UUID4) -> VideoResponse:
    category = videos.join(categories).join(users)
    extract_query = (
        select(
            [videos, categories.c.title.label("category"), users.c.email.label("owner")]
        )
        .select_from(category)
        .where(videos.c.id == video_id)
    )
    stored_video = await database.fetch_one(extract_query)

    return VideoResponse(**stored_video)


async def create(video_data: VideoUpload) -> VideoResponse:
    insert_query = videos.insert().values(**video_data.dict()).returning(videos.c.id)
    video_id = await database.execute(insert_query)

    return await get_joined_by_id(video_id)


async def save_video(video_file: UploadFile) -> str:
    file_data = await video_file.read()

    file_path = generate_file_path(video_file.filename)
    with open(file_path, "wb") as f:
        f.write(file_data)

    return file_path


async def stream_file(file_path: str) -> Generator[bytes, None, None]:
    return read_by_chunks(file_path)
