import enum
import uuid
from sqlalchemy import String, Enum, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from app.domain.entities.base import BaseEntity

if TYPE_CHECKING:
    from app.domain.entities.user import User


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(BaseEntity):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[CategoryType] = mapped_column(Enum(CategoryType), nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # Hex color
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=True,
        index=True
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", "type", name="uq_category_user_name_type"),
    )

    def __repr__(self) -> str:
        return f"<Category(name={self.name}, type={self.type}, is_default={self.is_default})>"
