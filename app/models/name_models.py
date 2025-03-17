from typing import Optional
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import validator
from sqlalchemy.sql import func

def check_name(value:str) -> str:
    if not value or not value.strip():
        raise ValueError("Name must not be empty")
    return value.strip()

class NameBase(SQLModel):
    name: str = Field(max_length = 255)
    _name = validator("name",allow_reuse=True)(check_name)
    
class NameCreate(NameBase):
    pass
class NameRecord(NameBase, table=True):
    """
    名称记录数据库模型，用于在数据库中存储记录
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        max_length=36
    )
    created_at: Optional[int] = Field(
        default_factory=lambda: int(datetime.utcnow().timestamp()),
        sa_column=func.UNIX_TIMESTAMP()
    )
    # updated_at: Optional[int] = Field(
    #     default=None,
    #     sa_column=func.UNIX_TIMESTAMP()
    # )