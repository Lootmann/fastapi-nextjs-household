from datetime import datetime

from pydantic import BaseModel


class HouseholdBase(BaseModel):
    amount: int
    category_id: int
    registered_at: datetime

    class Config:
        orm_mode = True


class HouseholdCreate(HouseholdBase):
    pass


class HouseholdCreateResponse(HouseholdCreate):
    id: int


class Household(HouseholdBase):
    id: int
    user_id: int
