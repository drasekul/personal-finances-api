import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieve a user by their UUID."""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their unique email."""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, user: User) -> User:
        """Create a new user in the system."""
        self.db.add(user)
        await self.db.flush()
        return user

    async def update(self, user: User) -> User:
        """Update an existing user."""
        await self.db.flush()
        return user

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination."""
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
