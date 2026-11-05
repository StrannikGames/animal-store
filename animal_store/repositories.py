from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from animal_store.models import AnimalModel, UserModel


class UserRepository:
    async def find_by_login(
        self, login: str, session: AsyncSession
    ) -> UserModel | None:
        q = select(UserModel).where(UserModel.login == login)
        s = await session.execute(q)
        return s.scalar_one_or_none()

    async def find_by_id(self, user_id: int, session: AsyncSession) -> UserModel | None:
        return await session.get(UserModel, user_id)

    async def create(
        self, name: str, login: str, password_hash: str, session: AsyncSession
    ) -> UserModel:
        user = UserModel(name=name, login=login, password_hash=password_hash)
        session.add(user)
        await session.commit()
        return user


class AnimalRepository:
    async def find_all(
        self, session: AsyncSession, name: str | None = None, type: str | None = None
    ) -> list[AnimalModel]:
        q = select(AnimalModel).order_by(AnimalModel.id)
        if name is not None:
            q = q.where(AnimalModel.name.ilike(f"%{name}%"))
        if type is not None:
            q = q.where(AnimalModel.type == type)
        s = await session.execute(q)
        return list(s.scalars().all())

    async def find_by_id(
        self, animal_id: int, session: AsyncSession
    ) -> AnimalModel | None:
        return await session.get(AnimalModel, animal_id)

    async def create(self, type: str, name: str, session: AsyncSession) -> AnimalModel:
        animal = AnimalModel(type=type, name=name)
        session.add(animal)
        await session.commit()
        return animal

    async def update(
        self, animal: AnimalModel, type: str, name: str, session: AsyncSession
    ) -> AnimalModel:
        animal.type = type
        animal.name = name
        await session.commit()
        return animal

    async def delete(self, animal: AnimalModel, session: AsyncSession) -> None:
        await session.delete(animal)
        await session.commit()
