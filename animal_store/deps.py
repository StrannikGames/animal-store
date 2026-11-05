from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from animal_store import config
from animal_store.db import DatabaseManager
from animal_store.models import UserModel
from animal_store.repositories import AnimalRepository, UserRepository
from animal_store.security import PasswordHasher, TokenManager

db_manager = DatabaseManager(config.DATABASE_URL)
password_hasher = PasswordHasher()
token_manager = TokenManager(config.SECRET_KEY, config.TOKEN_LIFETIME)
user_repository = UserRepository()
animal_repository = AnimalRepository()

SessionDep = Annotated[AsyncSession, Depends(db_manager.session_dependency)]

BearerSchema = HTTPBearer(auto_error=False)


async def authenticate_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(BearerSchema)],
    session: SessionDep,
) -> UserModel:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    user_id = token_manager.verify_token(credentials.credentials)
    if user_id is None:
        raise unauthorized

    user = await user_repository.find_by_id(user_id, session)
    if user is None:
        raise unauthorized

    return user


CurrentUserDep = Annotated[UserModel, Depends(authenticate_user)]
