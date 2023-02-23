from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.categories as category_crud
import api.schemas.categories as category_schema
from api.cruds import auths as auth_api
from api.db import get_db
from api.models import users as user_model

router = APIRouter()


@router.get(
    "/categories",
    response_model=List[category_schema.Category],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth_api.get_current_active_user),
):
    return await category_crud.get_categories(db, current_user.id)


@router.get(
    "/categories/{category_id}",
    response_model=category_schema.Category,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(auth_api.get_current_active_user),
):
    category = await category_crud.find_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category<{category_id}> Not Found")
    return category


@router.post(
    "/categories",
    response_model=category_schema.CategoryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_body: category_schema.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(auth_api.get_current_active_user),
):
    return await category_crud.create_categories(db, category_body, current_user.id)


@router.patch(
    "/categories/{category_id}",
    response_model=category_schema.CategoryCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category_id: int,
    category_body: category_schema.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(auth_api.get_current_active_user),
):
    category = await category_crud.find_by_id(db, category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category<{category_id}> Not Found"
        )

    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Authenticated")

    return await category_crud.update_category(db, category_body, updated=category)


@router.delete("/categories/{category_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: user_model.User = Depends(auth_api.get_current_active_user),
):
    category = await category_crud.find_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail=f"Category<{category_id}> Not Found")

    await category_crud.delete_category(db, category)
