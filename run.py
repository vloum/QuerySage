import argparse
from app.langchain.utils import MakeFastAPIOffline
from configs import OPEN_CROSS_DOMAIN, VERSION, NLTK_DATA_PATH
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import nltk

# 导入路由模块
from app.router import mount_app_routes


nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

def create_app(run_mode: str = None):
    app = FastAPI(
        title="Langchain-Chatchat API Server",
        version=VERSION
    )
    MakeFastAPIOffline(app)

    # Add CORS middleware to allow all origins
    # 在config.py中设置OPEN_DOMAIN=True，允许跨域
    # set OPEN_DOMAIN=True in config.py to allow cross-domain
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    mount_app_routes(app, run_mode=run_mode)
    return app

# 主程序入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='QuerySage',
                                     description='智者')
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9999)
    # 初始化消息
    args = parser.parse_args()
    args_dict = vars(args)

    app = create_app()
    uvicorn.run('run:create_app', host=args.host, port=args.port, reload=True)
