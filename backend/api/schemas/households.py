from datetime import datetime

from pydantic import BaseModel, Field

from api.schemas.categories import Category


class HouseholdBase(BaseModel):
    amount: int
    category: Category = Field(None, alias="Category")
    registered_at: datetime

    class Config:
        orm_mode = True


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdCreateResponse(HouseholdCreate):
    id: int


class Household(HouseholdBase):
    id: int
