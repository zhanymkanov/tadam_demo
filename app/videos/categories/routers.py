from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.service import get_jwt_user_active

from . import service
from .constants import ErrorCode
from .models import Category

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Category)
async def post_category(
    category_data: Category,
    user=Depends(get_jwt_user_active),
):
    if not user.get("is_superuser"):  # TODO only superusers can add
        pass

    return await service.create(category_data)


@router.post(
    "/{category_slug}", status_code=status.HTTP_200_OK, response_model=Category
)
async def get_category(
    category_slug: str,
):
    category = await service.get_by_slug(category_slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.CATEGORY_NOT_FOUND,
        )

    return category
