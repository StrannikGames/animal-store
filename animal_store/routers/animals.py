from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import PositiveInt, StringConstraints

from animal_store.deps import CurrentUserDep, SessionDep, animal_repository
from animal_store.models import AnimalModel
from animal_store.schemas import (
    AnimalCreateSchema,
    AnimalSchema,
    AnimalType,
    AnimalUpdateSchema,
)

router = APIRouter(prefix="/animals", tags=["animals"])


async def get_animal_or_404(animal_id: int, session) -> AnimalModel:
    animal = await animal_repository.find_by_id(animal_id, session)
    if animal is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Животное не найдено")
    return animal


@router.get("")
async def get_all_animals(
    session: SessionDep,
    name: Annotated[str, StringConstraints(max_length=30)] | None = None,
    type: AnimalType | None = None,
) -> list[AnimalSchema]:
    animals = await animal_repository.find_all(session, name=name, type=type)
    return [AnimalSchema.model_validate(a) for a in animals]


@router.get("/{id}")
async def get_animal_by_id(id: PositiveInt, session: SessionDep) -> AnimalSchema:
    return AnimalSchema.model_validate(await get_animal_or_404(id, session))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_animal(
    body: AnimalCreateSchema, session: SessionDep, _: CurrentUserDep
) -> AnimalSchema:
    animal = await animal_repository.create(
        type=body.type, name=body.name, session=session
    )
    return AnimalSchema.model_validate(animal)


@router.put("/{id}")
async def update_animal(
    id: PositiveInt, body: AnimalUpdateSchema, session: SessionDep, _: CurrentUserDep
) -> AnimalSchema:
    animal = await get_animal_or_404(id, session)
    animal = await animal_repository.update(
        animal, type=body.type, name=body.name, session=session
    )
    return AnimalSchema.model_validate(animal)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(
    id: PositiveInt, session: SessionDep, _: CurrentUserDep
) -> Response:
    animal = await get_animal_or_404(id, session)
    await animal_repository.delete(animal, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
