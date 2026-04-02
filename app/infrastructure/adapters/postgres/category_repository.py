import uuid
from typing import Optional, List
from sqlalchemy import select, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.category import Category, CategoryType
from app.domain.entities.user_category_preference import UserCategoryPreference
from app.domain.ports.category_repository import CategoryRepository


class SQLAlchemyCategoryRepository(CategoryRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalars().first()

    async def get_by_name(self, name: str, user_id: Optional[uuid.UUID], type: CategoryType) -> Optional[Category]:
        result = await self.session.execute(
            select(Category).where(
                and_(
                    Category.name == name,
                    Category.user_id == user_id,
                    Category.type == type
                )
            )
        )
        return result.scalars().first()

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def update(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(Category).where(Category.id == category_id)
        )
        return result.rowcount > 0

    async def list_for_user(self, user_id: uuid.UUID, include_defaults: bool = True) -> List[Category]:
        # Get disabled default category IDs
        disabled_ids = await self.get_disabled_category_ids(user_id)
        
        query = select(Category).where(
            or_(
                Category.user_id == user_id,
                and_(
                    Category.user_id == None,
                    Category.is_default == True,
                    ~Category.id.in_(disabled_ids) if disabled_ids else True
                )
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_defaults(self) -> List[Category]:
        result = await self.session.execute(
            select(Category).where(Category.user_id == None)
        )
        return list(result.scalars().all())

    async def set_preference(self, user_id: uuid.UUID, category_id: uuid.UUID, is_enabled: bool) -> None:
        # Check if exists
        result = await self.session.execute(
            select(UserCategoryPreference).where(
                and_(
                    UserCategoryPreference.user_id == user_id,
                    UserCategoryPreference.category_id == category_id
                )
            )
        )
        pref = result.scalars().first()
        
        if pref:
            pref.is_enabled = is_enabled
        else:
            pref = UserCategoryPreference(
                user_id=user_id,
                category_id=category_id,
                is_enabled=is_enabled
            )
            self.session.add(pref)
        
        await self.session.flush()

    async def get_disabled_category_ids(self, user_id: uuid.UUID) -> List[uuid.UUID]:
        result = await self.session.execute(
            select(UserCategoryPreference.category_id).where(
                and_(
                    UserCategoryPreference.user_id == user_id,
                    UserCategoryPreference.is_enabled == False
                )
            )
        )
        return list(result.scalars().all())
