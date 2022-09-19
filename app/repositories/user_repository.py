from typing import Optional, List

from sqlalchemy import select, update, delete

from app import models
from app import schemas
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash


class UserRepository(BaseRepository):

    _model = models.User
    _schema = schemas.User

    async def find(self, id: int) -> Optional[schemas.User]:
        entry = await self._session.get(self._model, id)
        return self._schema.from_orm(entry) if entry else None

    async def find_by_email(self, email: str) -> Optional[schemas.User]:
        query = select(self._model).filter_by(email=email)
        entry = await self._session.execute(query)
        user = entry.scalars().one_or_none()
        return self._schema.from_orm(user) if user else None

    async def get(self, **filters) -> List[schemas.User]:
        query = select(self._model).filter_by(**filters)
        entries = await self._session.execute(query)
        return list(map(lambda e: self._schema.from_orm(e), entries.scalars().all())) if entries else []

    async def create(self, fields: schemas.CreateUser) -> schemas.User:
        params = {**fields.dict(), 'password': get_password_hash(fields.password)}
        entry = self._model(**params)
        self._session.add(entry)
        await self._session.commit()
        await self._session.refresh(entry)
        return self._schema.from_orm(entry)

    async def update(self, id: int, fields: schemas.UpdateUser) -> Optional[schemas.User]:
        params = {**fields.dict(), 'password': get_password_hash(fields.password)}
        query = update(self._model).where(self._model.id == id). \
            values(**params).returning(self._model)
        affected = await self._session.execute(select(self._model).from_statement(query))
        user = affected.scalars().one_or_none()
        return self._schema.from_orm(user) if user else None

    async def delete(self, id: int) -> List:
        query = delete(self._model).where(self._model.id == id).execution_options(synchronize_session="fetch")
        affected = await self._session.execute(query)
        print(affected.scalars().all())
        return affected