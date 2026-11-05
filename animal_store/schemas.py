from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

AnimalType = Literal["cat", "dog"]
AnimalName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)
]


#животные


class AnimalCreateSchema(BaseModel):
    type: AnimalType
    name: AnimalName


class AnimalUpdateSchema(BaseModel):
    type: AnimalType
    name: AnimalName


class AnimalSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: AnimalType
    name: str


#пользователи

UserName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
]
Login = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]+$",
    ),
]
Password = Annotated[str, StringConstraints(min_length=8, max_length=64)]


class UserRegisterSchema(BaseModel):
    name: UserName
    login: Login
    password: Password


class UserLoginSchema(BaseModel):
    login: Login
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    login: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
