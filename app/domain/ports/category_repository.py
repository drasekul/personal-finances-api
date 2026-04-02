import uuid
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.category import Category, CategoryType


class CategoryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        """Retrieve a category by its UUID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str, user_id: Optional[uuid.UUID], type: CategoryType) -> Optional[Category]:
        """Retrieve a category by name, user_id (or None for default), and type."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, category: Category) -> Category:
        """Update an existing category."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, category_id: uuid.UUID) -> bool:
        """Delete a category."""
        raise NotImplementedError

    @abstractmethod
    async def list_for_user(self, user_id: uuid.UUID, include_defaults: bool = True) -> List[Category]:
        """List all categories available for a user, including defaults by default."""
        raise NotImplementedError

    @abstractmethod
    async def list_defaults(self) -> List[Category]:
        """List all system-wide default categories."""
        raise NotImplementedError

    @abstractmethod
    async def set_preference(self, user_id: uuid.UUID, category_id: uuid.UUID, is_enabled: bool) -> None:
        """Set user preference (enable/disable) for a default category."""
        raise NotImplementedError

    @abstractmethod
    async def get_disabled_category_ids(self, user_id: uuid.UUID) -> List[uuid.UUID]:
        """Get IDs of default categories disabled by the user."""
        raise NotImplementedError
