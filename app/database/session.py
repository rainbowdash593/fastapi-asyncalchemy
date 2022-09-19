from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.settings import settings

async_engine = create_async_engine(settings.DATABASE_DSN)
session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)