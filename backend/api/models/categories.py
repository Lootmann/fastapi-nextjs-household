from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base
from api.models.households import Household


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # Household
    households: Mapped[List["Household"]] = relationship(back_populates="category")

    # User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Category (id, name) = ({self.id}, {self.name})>"
