import uuid
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieve a user by their UUID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their unique email."""
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user in the system."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination."""
        raise NotImplementedError
