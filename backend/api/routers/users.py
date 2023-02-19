from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import users as user_api
from api.db import get_db
from api.schemas import users as user_schema

router = APIRouter()


@router.get(
    "/users",
    response_model=List[user_schema.User],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_api.get_all_users(db)
