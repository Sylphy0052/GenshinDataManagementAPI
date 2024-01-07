from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.db import Base
from api.models.user import User  # noqa
from api.settings import DB_URL

engine = create_engine(DB_URL, echo=True)


def _init_db() -> None:
    """データベースのセッションを初期化し、デフォルトの状態に設定します。

    注意：この関数は通常、データベースをリセットした後や
    アプリケーションが起動するときに内部的に呼び出されます。
    """
    session_ = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with session_() as session:
        # データベースの初期化処理を記述します。
        session.commit()


def reset_db() -> None:
    """データベースを初期状態にリセットします。

    注意：この関数は開発目的で用意されており、本番環境での使用には注意が必要です。
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _init_db()


if __name__ == "__main__":
    reset_db()
