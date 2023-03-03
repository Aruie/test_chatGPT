import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

import aiosqlite

# SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# @contextlib.contextmanager
# async def get_db() -> AsyncSession:
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


