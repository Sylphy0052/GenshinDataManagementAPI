from sqlalchemy import Column, Integer, String

from api.db import Base
from api.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name})>"
