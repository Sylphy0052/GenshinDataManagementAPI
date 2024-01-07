from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.settings import ASYNC_DB_URL

engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)  # type: ignore

Base = declarative_base()


async def get_db() -> AsyncGenerator[None, AsyncSession]:
    """非同期データベースセッションを提供するジェネレータ関数です。
    Returns:
        AsyncGenerator[None, AsyncSession]: 非同期セッションのジェネレータ
    Raises:
        - ジェネレータがセッションの生成に失敗した場合、適切な例外が発生します。
    """
    async with async_session() as session:  # type: ignore
        yield session
