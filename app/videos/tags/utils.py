from typing import Optional, Tuple

from fastapi import Form, HTTPException, status
from slugify import slugify

from app.utils import generate_name

from .constants import ErrorCode
from .models import Tag


def clean_tags(tags: Optional[str] = Form(None)) -> Optional[Tuple[Tag]]:
    if not tags:
        return

    tags = set(tag.strip() for tag in tags.split(","))

    if len(tags) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.TOO_MANY_TAGS,
        )

    return tuple(
        Tag(title=tag, slug=f"{slugify(tag)}-{generate_name(6)}") for tag in tags
    )
