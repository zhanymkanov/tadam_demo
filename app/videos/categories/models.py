import uuid

from pydantic import UUID4, BaseModel, Field


class Category(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    title: str
    slug: str
