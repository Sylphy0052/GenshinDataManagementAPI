import logging
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from api.schemas.user import UserCreate, UserUpdate
from api.settings import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


async def get_users(db: AsyncSession, page: int, limit: int, name: str | None) -> list[User]:
    """指定された条件に基づいてユーザーのリストを非同期で取得します。
    Args:
        db (AsyncSession): データベースセッションオブジェクト。
        page (int): 取得するページ番号。1以上の整数を指定します。
        limit (int): 1ページあたりのユーザー数の上限。1以上の整数を指定します。
        name (str | None): 検索するユーザー名の一部。Noneまたは文字列を指定します。
    Returns:
        list[User]: 条件に一致するユーザーオブジェクトのリストを返します。
    """
    stmt = select(User)
    if name is not None:
        stmt = stmt.where(User.name.contains(name))
    stmt = stmt.order_by(User.id).offset((page - 1) * limit).limit(limit)
    result = await db.execute(stmt)
    return [user for user in result.scalars().all()]


async def create_users(db: AsyncSession, body: UserCreate) -> User:
    """新しいユーザをデータベースに登録します。
    Args:
        db (AsyncSession): データベースセッションオブジェクト。
        body (UserCreate): 登録するユーザの情報を含むオブジェクト。
    Returns:
        User: データベースに登録されたユーザオブジェクト。
    Raises:
        HTTPException: ユーザ登録中にエラーが発生した場合、HTTPステータスコード500で例外を発生させます。
    """
    try:
        user = User(name=body.name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"ユーザの登録に失敗しました\n{e}")
    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    """指定されたユーザIDのユーザ情報を取得します。
    Args:
        db (AsyncSession): データベースセッションオブジェクト。
        user_id (int): 取得するユーザーのID。
    Returns:
        User: 指定されたIDのユーザーオブジェクト。
    Raises:
        HTTPException: 指定されたIDのユーザーが見つからなかった場合、HTTPステータスコード404で例外を発生させます。
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"ユーザーID {user_id} のユーザーが見つかりません")
    return user


async def update_user(db: AsyncSession, user_id: int, body: UserUpdate) -> User:
    """指定されたユーザIDのユーザ情報を更新します。
    Args:
        db (AsyncSession): データベースセッションオブジェクト。
        user_id (int): 更新するユーザーのID。
        body (UserUpdate): 更新するユーザーの情報を含むオブジェクト。
    Returns:
        User: 更新されたユーザーオブジェクト。
    Raises:
        HTTPException: 指定されたIDのユーザーが見つからなかった場合、HTTPステータスコード404で例外を発生させます。
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"ユーザーID {user_id} のユーザーが見つかりません")
    user.name = body.name  # type: ignore
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """指定されたユーザIDのユーザ情報を削除します。
    Args:
        db (AsyncSession): データベースセッションオブジェクト。
        user_id (int): 削除するユーザーのID。
    Raises:
        HTTPException: 指定されたIDのユーザーが見つからなかった場合、HTTPステータスコード404で例外を発生させます。
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"ユーザーID {user_id} のユーザーが見つかりません")
    await db.delete(user)
    await db.commit()
