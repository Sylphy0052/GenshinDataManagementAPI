from fastapi import Body
from pydantic import BaseModel


# Requestモデルの定義
class UserCreate(BaseModel):
    name: str = Body(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "user1",
            }
        }
    }


class UserUpdate(BaseModel):
    name: str = Body(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "user1",
            }
        }
    }


# Responseモデルの定義
class User(BaseModel):
    id: int
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "user1",
            }
        }
    }
