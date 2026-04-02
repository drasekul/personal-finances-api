import uuid
from typing import List, Optional
from app.domain.entities.tag import Tag
from app.domain.ports.tag_repository import TagRepository
from app.domain.exceptions import DomainException, EntityNotFoundException


class TagUseCase:
    def __init__(self, tag_repo: TagRepository):
        self.tag_repo = tag_repo

    async def get_tags(self, user_id: uuid.UUID) -> List[Tag]:
        return await self.tag_repo.list_for_user(user_id)

    async def create_tag(
        self, 
        user_id: uuid.UUID, 
        name: str, 
        color: Optional[str] = None
    ) -> Tag:
        existing = await self.tag_repo.get_by_name(name, user_id)
        if existing:
            raise DomainException(f"Tag '{name}' already exists for this user.")

        tag = Tag(
            name=name,
            color=color,
            user_id=user_id
        )
        return await self.tag_repo.create(tag)

    async def update_tag(
        self,
        user_id: uuid.UUID,
        tag_id: uuid.UUID,
        name: Optional[str] = None,
        color: Optional[str] = None
    ) -> Tag:
        tag = await self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise EntityNotFoundException("Tag", tag_id)
        
        if tag.user_id != user_id:
            raise DomainException("Not authorized to update this tag.")

        if name:
            existing = await self.tag_repo.get_by_name(name, user_id)
            if existing and existing.id != tag_id:
                raise DomainException(f"Tag '{name}' already exists.")
            tag.name = name
        
        if color is not None:
            tag.color = color

        return await self.tag_repo.update(tag)

    async def delete_tag(self, user_id: uuid.UUID, tag_id: uuid.UUID) -> bool:
        tag = await self.tag_repo.get_by_id(tag_id)
        if not tag:
            raise EntityNotFoundException("Tag", tag_id)
        
        if tag.user_id != user_id:
            raise DomainException("Not authorized to delete this tag.")

        return await self.tag_repo.delete(tag_id)
