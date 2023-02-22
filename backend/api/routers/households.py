from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import auths as auth_api
from api.cruds import households as household_crud
from api.db import get_db
from api.models import households as household_model
from api.models import users as user_model
from api.schemas import households as household_schema

router = APIRouter()


@router.get(
    "/households",
    response_model=List[household_schema.Household],
    status_code=status.HTTP_200_OK,
)
async def get_households(
    db: AsyncSession = Depends(get_db),
    _=Depends(auth_api.get_current_active_user),
):
    return await household_crud.get_households(db)


@router.post(
    "/households",
    response_model=household_schema.HouseholdCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    household_body: household_schema.HouseholdCreate,
    db: AsyncSession = Depends(get_db),
    current_user: user_model.User = Depends(auth_api.get_current_active_user),
):
    return await household_crud.create_households(db, household_body, current_user.id)
