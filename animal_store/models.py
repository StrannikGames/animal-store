from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    login: Mapped[str]= mapped_column(String(32), unique=True, index=True)
    password_hash: Mapped[str]


class AnimalModel(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] =mapped_column(String(10))
    name: Mapped[str] =mapped_column(String(30))
