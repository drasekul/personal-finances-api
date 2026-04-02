import uuid
from sqlalchemy import ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.entities.base import BaseEntity


class UserCategoryPreference(BaseEntity):
    __tablename__ = "user_category_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "category_id", name="uq_user_category_preference"),
    )

    def __repr__(self) -> str:
        return f"<UserCategoryPreference(user_id={self.user_id}, category_id={self.category_id}, enabled={self.is_enabled})>"
