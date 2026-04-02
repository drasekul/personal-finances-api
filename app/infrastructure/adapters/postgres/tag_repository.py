import uuid
from typing import Optional, List
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.tag import Tag
from app.domain.ports.tag_repository import TagRepository


class SQLAlchemyTagRepository(TagRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, tag_id: uuid.UUID) -> Optional[Tag]:
        result = await self.session.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return result.scalars().first()

    async def get_by_name(self, name: str, user_id: uuid.UUID) -> Optional[Tag]:
        result = await self.session.execute(
            select(Tag).where(
                and_(
                    Tag.name == name,
                    Tag.user_id == user_id
                )
            )
        )
        return result.scalars().first()

    async def create(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        await self.session.refresh(tag)
        return tag

    async def update(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        await self.session.refresh(tag)
        return tag

    async def delete(self, tag_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(Tag).where(Tag.id == tag_id)
        )
        return result.rowcount > 0

    async def list_for_user(self, user_id: uuid.UUID) -> List[Tag]:
        result = await self.session.execute(
            select(Tag).where(Tag.user_id == user_id)
        )
        return list(result.scalars().all())
