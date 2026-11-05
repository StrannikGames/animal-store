from fastapi import APIRouter, HTTPException, status

from animal_store.deps import (
    CurrentUserDep,
    SessionDep,
    password_hasher,
    token_manager,
    user_repository,
)
from animal_store.schemas import (
    TokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserSchema,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: UserRegisterSchema, session: SessionDep) -> UserSchema:
    # Проверка на существование пользователя с таким логином
    if await user_repository.find_by_login(body.login, session) is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином уже существует",
        )

    user = await user_repository.create(
        name=body.name,
        login=body.login,
        password_hash=password_hasher.get_password_hash(body.password),
        session=session,
    )
    return UserSchema.model_validate(user)


@router.post("/login")
async def login(body: UserLoginSchema, session: SessionDep) -> TokenSchema:
    user = await user_repository.find_by_login(body.login, session)
    if user is None or not password_hasher.compare_passwords(
        body.password, user.password_hash
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
        )

    return TokenSchema(access_token=token_manager.issue_token(user.id))


@router.get("/me")
async def get_me(user: CurrentUserDep) -> UserSchema:
    return UserSchema.model_validate(user)
