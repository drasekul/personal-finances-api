import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.infrastructure.adapters.postgres.category_repository import SQLAlchemyCategoryRepository
from app.application.use_cases.category import CategoryUseCase
from app.web.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryToggle
from app.web.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions import DomainException, EntityNotFoundException

router = APIRouter(prefix="/categories", tags=["Categories"])


async def get_category_use_case(db: AsyncSession = Depends(get_db)) -> CategoryUseCase:
    repo = SQLAlchemyCategoryRepository(db)
    return CategoryUseCase(repo)


@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    current_user: User = Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """List all categories available for the current user."""
    return await use_case.get_categories(current_user.id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """Create a new custom category."""
    try:
        return await use_case.create_category(
            user_id=current_user.id,
            name=category_in.name,
            type=category_in.type,
            icon=category_in.icon,
            color=category_in.color
        )
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: uuid.UUID,
    category_in: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """Update a custom category."""
    try:
        return await use_case.update_category(
            user_id=current_user.id,
            category_id=category_id,
            name=category_in.name,
            icon=category_in.icon,
            color=category_in.color
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """Delete a custom category."""
    try:
        await use_case.delete_category(current_user.id, category_id)
        return None
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/toggle-default", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_default_category(
    toggle: CategoryToggle,
    current_user: User = Depends(get_current_user),
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """Enable or disable a system default category for the current user."""
    try:
        await use_case.toggle_default_category(
            user_id=current_user.id,
            category_id=toggle.category_id,
            enabled=toggle.enabled
        )
        return None
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/seed", response_model=List[CategoryResponse], include_in_schema=False)
async def seed_categories(
    use_case: CategoryUseCase = Depends(get_category_use_case)
):
    """Seed initial system categories. Internal use only."""
    return await use_case.seed_default_categories()
