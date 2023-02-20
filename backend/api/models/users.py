from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.categories import Category
from api.models.households import Household


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]

    # categories
    categories: Mapped[List["Category"]] = relationship("Category", backref="user")

    # households
    households: Mapped[List["Household"]] = relationship("Household", backref="user")

    def __repr__(self) -> str:
        return f"<User ({self.id}, {self.name})>"
