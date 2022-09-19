from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user, get_current_superuser

from app import schemas
from app.repositories import UserRepository

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def get(
        db: AsyncSession = Depends(get_db),
        current_superuser: schemas.User = Depends(get_current_superuser)
) -> List[schemas.User]:
    repo = UserRepository(db)
    users = await repo.get()
    return users


@router.get("/me", response_model=schemas.User)
async def me(
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
async def find(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_superuser: schemas.User = Depends(get_current_superuser)
) -> schemas.User:
    repo = UserRepository(db)
    user = await repo.find(user_id)
    return user


@router.put("/", response_model=schemas.User)
async def create(
        dto: schemas.CreateUser,
        db: AsyncSession = Depends(get_db)
) -> schemas.User:
    repo = UserRepository(db)
    user = await repo.find_by_email(dto.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    created_user = await repo.create(dto)
    return created_user


@router.post("/{user_id}", response_model=schemas.User)
async def update(
        user_id: int,
        dto: schemas.UpdateUser,
        db: AsyncSession = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if not current_user.is_superuser and user_id != current_user.id:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    repo = UserRepository(db)
    updated_user = await repo.update(user_id, dto)
    return updated_user


@router.delete("/{user_id}", response_model=bool)
async def delete(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_superuser: schemas.User = Depends(get_current_superuser)
) -> bool:
    repo = UserRepository(db)
    affected = await repo.delete(int(user_id))
    return bool(affected)
