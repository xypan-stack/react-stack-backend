from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.name_models import NameCreate, NameRecord
from database.connection import get_session

router = APIRouter(
    prefix="/api",
    tags=["names"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/names", response_model=NameRecord)
async def create_name(
    name_create: NameCreate,
    session: Session = Depends(get_session)
):
    """
    创建新的名称记录，不再通过 WebSocket 推送消息。
    """
    # 根据客户端数据创建新的记录
    name_record = NameRecord(name=name_create.name)
    session.add(name_record)
    try:
        session.commit()
        session.refresh(name_record)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error saving name") from e

    return name_record

@router.get("/names", response_model=list[NameRecord])
async def read_names(
    session: Session = Depends(get_session)
):
    """
    获取所有名称记录
    """
    names = session.exec(select(NameRecord)).all()
    return names