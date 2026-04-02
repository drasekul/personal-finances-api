import uuid
from typing import List, Optional
from app.domain.entities.category import Category, CategoryType
from app.domain.ports.category_repository import CategoryRepository
from app.domain.exceptions import DomainException, EntityNotFoundException


class CategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_categories(self, user_id: uuid.UUID) -> List[Category]:
        return await self.category_repo.list_for_user(user_id)

    async def create_category(
        self, 
        user_id: uuid.UUID, 
        name: str, 
        type: CategoryType, 
        icon: Optional[str] = None, 
        color: Optional[str] = None
    ) -> Category:
        # Check if category with same name and type exists for this user
        existing = await self.category_repo.get_by_name(name, user_id, type)
        if existing:
            raise DomainException(f"Category '{name}' of type '{type}' already exists for this user.")

        category = Category(
            name=name,
            type=type,
            icon=icon,
            color=color,
            user_id=user_id,
            is_default=False
        )
        return await self.category_repo.create(category)

    async def update_category(
        self,
        user_id: uuid.UUID,
        category_id: uuid.UUID,
        name: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None
    ) -> Category:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException("Category", category_id)
        
        if category.is_default:
            raise DomainException("Cannot update default system categories.")
        
        if category.user_id != user_id:
            raise DomainException("Not authorized to update this category.")

        if name:
            # Check for name collision
            existing = await self.category_repo.get_by_name(name, user_id, category.type)
            if existing and existing.id != category_id:
                raise DomainException(f"Category '{name}' already exists.")
            category.name = name
        
        if icon is not None:
            category.icon = icon
        if color is not None:
            category.color = color

        return await self.category_repo.update(category)

    async def delete_category(self, user_id: uuid.UUID, category_id: uuid.UUID) -> bool:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException("Category", category_id)
        
        if category.is_default:
            raise DomainException("Cannot delete default system categories. Use disable instead.")
        
        if category.user_id != user_id:
            raise DomainException("Not authorized to delete this category.")

        return await self.category_repo.delete(category_id)

    async def toggle_default_category(self, user_id: uuid.UUID, category_id: uuid.UUID, enabled: bool) -> None:
        category = await self.category_repo.get_by_id(category_id)
        if not category or not category.is_default:
            raise DomainException("Category not found or is not a default category.")
        
        await self.category_repo.set_preference(user_id, category_id, enabled)

    async def seed_default_categories(self) -> List[Category]:
        defaults = [
            # Expenses
            ("Food & Dining", CategoryType.EXPENSE, "utensils", "#FF5733"),
            ("Transportation", CategoryType.EXPENSE, "car", "#33FF57"),
            ("Housing", CategoryType.EXPENSE, "home", "#3357FF"),
            ("Utilities", CategoryType.EXPENSE, "bolt", "#F033FF"),
            ("Entertainment", CategoryType.EXPENSE, "film", "#FF33A1"),
            ("Healthcare", CategoryType.EXPENSE, "heart", "#33FFF5"),
            ("Shopping", CategoryType.EXPENSE, "shopping-cart", "#F5FF33"),
            ("Education", CategoryType.EXPENSE, "graduation-cap", "#FFA533"),
            ("Travel", CategoryType.EXPENSE, "plane", "#33A5FF"),
            ("Personal Care", CategoryType.EXPENSE, "user", "#A533FF"),
            # Income
            ("Salary", CategoryType.INCOME, "money-bill-wave", "#2ECC71"),
            ("Freelance", CategoryType.INCOME, "laptop-code", "#3498DB"),
            ("Investments", CategoryType.INCOME, "chart-line", "#F1C40F"),
            ("Gifts", CategoryType.INCOME, "gift", "#E67E22"),
            ("Other Income", CategoryType.INCOME, "plus", "#9B59B6"),
        ]
        
        created = []
        for name, ctype, icon, color in defaults:
            existing = await self.category_repo.get_by_name(name, None, ctype)
            if not existing:
                category = Category(
                    name=name,
                    type=ctype,
                    icon=icon,
                    color=color,
                    is_default=True,
                    user_id=None
                )
                created.append(await self.category_repo.create(category))
        
        return created
