import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db import Base


class Household(Base):
    __tablename__ = "households"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    registered_at: Mapped[datetime.datetime]

    # Category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="households")

    # User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Household (id, amount, registered_at) = ({self.id}, {self.amount}, {self.registered_at})>"
