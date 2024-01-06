
from fastapi import FastAPI

from app.router.chat import chat_routes

def mount_app_routes(app: FastAPI, run_mode: str = None):
    # 知识库相关接口
    chat_routes(app)
