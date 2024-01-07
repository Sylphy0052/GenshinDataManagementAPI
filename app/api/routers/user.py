import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import user as user_crud
from api.db import get_db
from api.schemas import user as user_schema
from api.schemas.create_schema import get_user_schema, get_user_schemas
from api.settings import LOGGER_NAME
from api.validates.user import check_get_users, check_post_users, check_put_user

router = APIRouter()
logger = logging.getLogger(LOGGER_NAME)


@router.get("/users", response_model=list[user_schema.User])
async def get_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    name: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[user_schema.User]:
    """ページネーションを使用して、ユーザ情報のリストを取得します"""
    # 入力チェック
    check_get_users(page, limit, name)
    # データベースからデータを取得
    users = await user_crud.get_users(db, page, limit, name)
    # スキーマの作成
    user_schemas = get_user_schemas(users)
    return user_schemas


@router.post("/users", response_model=user_schema.User, status_code=HTTPStatus.CREATED.value)
async def create_users(
    body: user_schema.UserCreate,
    db: AsyncSession = Depends(get_db),
) -> user_schema.User:
    """新しいユーザをデータベースに登録します"""
    # 入力チェック
    check_post_users(body)
    # データベースからデータを取得
    user = await user_crud.create_users(db, body)
    # スキーマの作成
    user_schema = get_user_schema(user)
    return user_schema


@router.get("/users/{user_id}", response_model=user_schema.User)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> user_schema.User:
    """指定されたユーザIDのユーザ情報を取得します"""
    # データベースからデータを取得
    user = await user_crud.get_user(db, user_id)
    # スキーマの作成
    user_schema = get_user_schema(user)
    return user_schema


@router.put("/users/{user_id}", response_model=user_schema.User)
async def update_user(
    user_id: int,
    body: user_schema.UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> user_schema.User:
    """指定されたユーザIDのユーザ情報を更新します"""
    # 入力チェック
    check_put_user(body)
    # データベースからデータを取得
    user = await user_crud.update_user(db, user_id, body)
    # スキーマの作成
    user_schema = get_user_schema(user)
    return user_schema


@router.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT.value)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """指定されたユーザIDのユーザ情報を削除します"""
    # データベースからデータを取得
    await user_crud.delete_user(db, user_id)
