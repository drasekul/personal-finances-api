import uuid
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.tag import Tag


class TagRepository(ABC):

    @abstractmethod
    async def get_by_id(self, tag_id: uuid.UUID) -> Optional[Tag]:
        """Retrieve a tag by its UUID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str, user_id: uuid.UUID) -> Optional[Tag]:
        """Retrieve a tag by name and user_id."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, tag: Tag) -> Tag:
        """Create a new tag."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, tag: Tag) -> Tag:
        """Update an existing tag."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, tag_id: uuid.UUID) -> bool:
        """Delete a tag."""
        raise NotImplementedError

    @abstractmethod
    async def list_for_user(self, user_id: uuid.UUID) -> List[Tag]:
        """List all tags owned by a user."""
        raise NotImplementedError
