from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.categories as category_crud
import api.schemas.categories as category_schema
from api.db import get_db

router = APIRouter()


@router.get("/categories", response_model=List[category_schema.Category])
async def categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_categories(db)


@router.post("/categories", response_model=category_schema.CategoryCreateResponse)
async def create_category(
    category_body: category_schema.CategoryCreate, db: AsyncSession = Depends(get_db)
):
    return await category_crud.create_categories(db, category_body)
@router.get("/categories/{category_id}")
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await category_crud.get_category(db, category_id)


