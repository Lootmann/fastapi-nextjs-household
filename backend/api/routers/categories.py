from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.categories as category_crud
import api.schemas.categories as category_schema
from api.db import get_db

router = APIRouter()


@router.get(
    "/categories",
    response_model=List[category_schema.Category],
    status_code=status.HTTP_200_OK,
)
async def categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_categories(db)


@router.get(
    "/categories/{category_id}",
    response_model=category_schema.Category,
    status_code=status.HTTP_200_OK,
)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category<{category_id}> Not Found")
    return category


@router.post(
    "/categories",
    response_model=category_schema.CategoryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_body: category_schema.CategoryCreate, db: AsyncSession = Depends(get_db)
):
    return await category_crud.create_categories(db, category_body)


@router.patch(
    "/categories/{category_id}",
    response_model=category_schema.CategoryCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category_id: int,
    category_body: category_schema.CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    category = await category_crud.get_category(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail=f"Category<{category_id}> Not Found")

    return await category_crud.update_category(db, category_body, updated=category[0])


@router.delete("/categories/{category_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await category_crud.get_category(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail=f"Category<{category_id}> Not Found")

    await category_crud.delete_category(db, category)
