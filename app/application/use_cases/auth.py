from typing import Optional, Tuple
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.domain.exceptions import DomainException


class AuthUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(
        self, email: str, password: str, full_name: str, currency: str = "USD"
    ) -> User:
        """Register a new user in the system."""
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise DomainException(f"User with email {email} already exists.")

        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            currency=currency,
        )
        return await self.user_repo.create(new_user)

    async def authenticate_user(
        self, email: str, password: str
    ) -> Tuple[str, str, User]:
        """Authenticate a user and return access and refresh tokens."""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise DomainException("Invalid email or password.")

        if not user.is_active:
            raise DomainException("User account is disabled.")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        return access_token, refresh_token, user

    async def refresh_access_token(self, refresh_token: str) -> Tuple[str, str, User]:
        """Verify a refresh token and return a new access token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise DomainException("Invalid refresh token.")

        user_id = payload.get("sub")
        if not user_id:
            raise DomainException("Invalid refresh token payload.")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise DomainException("User not found or disabled.")

        new_access_token = create_access_token(subject=str(user.id))
        new_refresh_token = create_refresh_token(subject=str(user.id))
        return new_access_token, new_refresh_token, user
