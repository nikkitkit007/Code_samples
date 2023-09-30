import subprocess
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings, ASYNC_DB_URL, SYNC_DB_URL


async_engine = create_async_engine(ASYNC_DB_URL, pool_size=5, echo=settings.DB_ECHO)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
sync_engine = create_engine(SYNC_DB_URL, echo=settings.DB_ECHO, pool_pre_ping=True)


def migrate():
    if subprocess.run(["alembic", "upgrade", 'head']).returncode > 0:
        raise Exception(f'DB migration failed')
