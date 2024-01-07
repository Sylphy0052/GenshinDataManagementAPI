from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped


class TimestampMixin:
    # 参考: https://qiita.com/tamanugi/items/9e3ac45f2657c2349e5b
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        """レコード作成日時"""
        return Column(DateTime, default=datetime.now(), nullable=False)  # type: ignore

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        """レコード更新日時"""
        return Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)  # type: ignore
