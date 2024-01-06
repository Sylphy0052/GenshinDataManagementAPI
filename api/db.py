from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.settings import ASYNC_DB_URL

engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)  # type: ignore

Base = declarative_base()


async def get_db() -> AsyncGenerator[None, AsyncSession]:
    """非同期データベースセッションを提供するジェネレータ関数です。

    この非同期関数は、コンテキストマネージャーを使用して非同期セッションを作成し、
    そのセッションを呼び出し元に提供します。セッションは `async with` ブロックによって
    自動的に閉じられるため、手動で閉じる必要はありません。

    使用例:
        async for session in get_db():
            # 非同期セッションを使用したデータベース操作
            ...

    戻り値:
        AsyncGenerator[None, AsyncSession]: 非同期セッションのジェネレータ

    例外:
        - ジェネレータがセッションの生成に失敗した場合、適切な例外が発生します。
    """
    async with async_session() as session:  # type: ignore
        yield session
