from http import HTTPStatus

from fastapi import HTTPException

from api.schemas import user as user_schema


def check_get_users(page: int, limit: int, name: str | None) -> None:
    """指定されたページ番号と制限数に基づいてユーザー情報を取得する前に、引数のバリデーションを行います。
    Args:
        page (int): 取得するページ番号。1以上の整数である必要があります。
        limit (int): 1ページあたりのユーザー数の上限。1以上の整数である必要があります。
        name (str | None): 検索するユーザー名。Noneまたは文字列である必要があります。
    Raises:
        HTTPException: 引数のバリデーションに失敗した場合に発生します。
    """
    # pageは1以上の整数であること
    if page < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ページ番号は1以上の整数である必要があります")
    if not isinstance(page, int):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ページ番号は整数である必要があります")
    # limitは1以上の整数であること
    if limit < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="制限数は1以上の整数である必要があります")
    if not isinstance(limit, int):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="制限数は整数である必要があります")
    # nameは文字列であること
    if name is not None and not isinstance(name, str):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ユーザー名は文字列である必要があります")


def check_post_users(body: user_schema.UserCreate) -> None:
    """ユーザー作成のリクエストボディのバリデーションを行います。
    Args:
        body (user_schema.UserCreate): ユーザー作成時に必要な情報が含まれたオブジェクト。
    Raises:
        HTTPException: 引数のバリデーションに失敗した場合に発生します。
    """
    # nameは1文字以上の文字であること
    if not isinstance(body.name, str):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ユーザー名は文字列である必要があります")
    if len(body.name) < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ユーザー名は1文字以上である必要があります")


def check_put_user(body: user_schema.UserUpdate) -> None:
    """ユーザー更新のリクエストボディのバリデーションを行います。
    Args:
        body (user_schema.UserUpdate): ユーザー更新時に必要な情報が含まれたオブジェクト。
    Raises:
        HTTPException: 引数のバリデーションに失敗した場合に発生します。
    """
    # nameは1文字以上の文字であること
    if not isinstance(body.name, str):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ユーザー名は文字列である必要があります")
    if len(body.name) < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ユーザー名は1文字以上である必要があります")
