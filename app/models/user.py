import uuid
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import DefaultClause
from sqlalchemy import Column, String, Boolean, Integer


class User(BaseModel):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, server_default=DefaultClause("0"), default=False, nullable=False)