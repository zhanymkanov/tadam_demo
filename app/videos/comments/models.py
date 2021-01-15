import uuid

from pydantic import UUID4, BaseModel, Field


class Comment(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    video_id: UUID4
    user_id: UUID4
    text: str
