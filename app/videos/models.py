import uuid
from typing import List

from pydantic import UUID4, BaseModel, Field

from app.videos.tags.models import Tag


class VideoBase(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    title: str
    description: str
    file_path: str


class VideoUpload(VideoBase):
    category_id: UUID4
    owner_id: UUID4


class VideoResponse(VideoBase):
    category: str
    owner: str
    tags: List[Tag] = None
