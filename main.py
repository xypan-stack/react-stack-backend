from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import names
from app.routers import websocket
from database.connection import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
# 注册 API 路由
app.include_router(names.router)
app.include_router(websocket.router)
