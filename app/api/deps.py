from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import schemas
from app.core import security
from app.core.settings import settings
from app.database.session import session
from app.repositories import UserRepository

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/access-token"
)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with session() as async_session:
        yield async_session
        await async_session.commit()


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> schemas.User:
    """
    Dependency function that get auth user by authorization header
    """
    repo = UserRepository(db)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await repo.find(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_superuser(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(reusable_oauth2)
):
    """
    Dependency function that validate auth user is super user
    """
    user = await get_current_user(db, token)
    if not user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user
