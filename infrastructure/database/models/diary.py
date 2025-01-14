from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from .users import User


class DiaryRecord(IdMixin, TimestampMixin, Base):
    __tablename__ = "diary_records"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="diary_records")

    score: Mapped[int]
