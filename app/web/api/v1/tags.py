import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.infrastructure.adapters.postgres.tag_repository import SQLAlchemyTagRepository
from app.application.use_cases.tag import TagUseCase
from app.web.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.web.dependencies.auth import get_current_user
from app.domain.entities.user import User
from app.domain.exceptions import DomainException, EntityNotFoundException

router = APIRouter(prefix="/tags", tags=["Tags"])


async def get_tag_use_case(db: AsyncSession = Depends(get_db)) -> TagUseCase:
    repo = SQLAlchemyTagRepository(db)
    return TagUseCase(repo)


@router.get("/", response_model=List[TagResponse])
async def list_tags(
    current_user: User = Depends(get_current_user),
    use_case: TagUseCase = Depends(get_tag_use_case)
):
    """List all tags owned by the current user."""
    return await use_case.get_tags(current_user.id)


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: TagCreate,
    current_user: User = Depends(get_current_user),
    use_case: TagUseCase = Depends(get_tag_use_case)
):
    """Create a new personal tag."""
    try:
        return await use_case.create_tag(
            user_id=current_user.id,
            name=tag_in.name,
            color=tag_in.color
        )
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: uuid.UUID,
    tag_in: TagUpdate,
    current_user: User = Depends(get_current_user),
    use_case: TagUseCase = Depends(get_tag_use_case)
):
    """Update a personal tag."""
    try:
        return await use_case.update_tag(
            user_id=current_user.id,
            tag_id=tag_id,
            name=tag_in.name,
            color=tag_in.color
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    use_case: TagUseCase = Depends(get_tag_use_case)
):
    """Delete a personal tag."""
    try:
        await use_case.delete_tag(current_user.id, tag_id)
        return None
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
