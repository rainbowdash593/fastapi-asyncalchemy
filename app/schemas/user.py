from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4
from app.schemas.base import BaseSchema


class User(BaseSchema):
    id: int
    uuid: UUID4
    email: str
    password: str
    is_superuser: bool


class CreateUser(BaseModel):
    email: str
    password: str


class UpdateUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None