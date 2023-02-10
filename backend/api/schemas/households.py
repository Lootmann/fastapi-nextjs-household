from datetime import datetime
from api.schemas.categories import Category

from pydantic import BaseModel, Field


class HouseholdBase(BaseModel):
    amount: int
    category: Category = Field(None, alias="Category")
    registered_at: datetime


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdCreateResponse(HouseholdCreate):
    id: int

    class Config:
        orm_mode = True


class Household(HouseholdBase):
    id: int

    class Config:
        orm_mode = True
