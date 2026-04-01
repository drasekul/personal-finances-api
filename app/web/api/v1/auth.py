from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.infrastructure.adapters.postgres.user_repository import SQLAlchemyUserRepository
from app.application.use_cases.auth import AuthUseCase
from app.web.schemas.user import UserCreate, UserResponse
from app.web.schemas.auth import LoginRequest, Token, RefreshTokenRequest
from app.domain.exceptions import DomainException

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_auth_use_case(db: AsyncSession = Depends(get_db)) -> AuthUseCase:
    user_repo = SQLAlchemyUserRepository(db)
    return AuthUseCase(user_repo)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_in: UserCreate, auth_use_case: AuthUseCase = Depends(get_auth_use_case)
):
    """
    Register a new user.
    """
    try:
        user = await auth_use_case.register_user(
            email=user_in.email,
            password=user_in.password,
            full_name=user_in.full_name,
            currency=user_in.currency,
        )
        return user
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    login_in: LoginRequest, auth_use_case: AuthUseCase = Depends(get_auth_use_case)
):
    """
    Authenticate user and get tokens.
    """
    try:
        access_token, refresh_token, user = await auth_use_case.authenticate_user(
            email=login_in.email, password=login_in.password
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user,
        }
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_in: RefreshTokenRequest,
    auth_use_case: AuthUseCase = Depends(get_auth_use_case),
):
    """
    Rotate tokens using a valid refresh token.
    """
    try:
        access_token, refresh_token, user = await auth_use_case.refresh_access_token(
            refresh_token=refresh_in.refresh_token
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user,
        }
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
