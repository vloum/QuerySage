
from fastapi import FastAPI

from app.router.chat import chat_routes
from app.router.document import parsing_docs

def mount_app_routes(app: FastAPI, run_mode: str = None):
    # 问答想相关接口
    chat_routes(app)

    # 文档类
    document_router(app)



def document_router(app: FastAPI):
    prefix_path = '/docs'

    app.post(f'{prefix_path}/parsing',
             tags=["docs"],
             summary="文档解析")(parsing_docs)