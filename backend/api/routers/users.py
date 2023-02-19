from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import users as user_api
from api.db import get_db
from api.schemas import users as user_schema

router = APIRouter()


@router.get("/users", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await user_api.get_all_users(db)


@router.post(
    "/users", response_model=user_schema.UserCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    found = await user_api.find_by_name(db, user_body.name)
    if found is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Duplicate Username: {user_body.name}"
        )
    return await user_api.create_user(db, user_body)


@router.get("/users/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_api.find_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User:{user_id} Not Found"
        )
    return user


@router.patch(
    "/users", response_model=user_schema.UserCreateResponse, status_code=status.HTTP_200_OK
)
async def update_user(user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    # TODO: get current user
    pass


@router.delete("/users", response_model=None, status_code=status.HTTP_200_OK)
async def delete_user(db: AsyncSession = Depends(get_db)):
    # TODO: get current user
    pass
