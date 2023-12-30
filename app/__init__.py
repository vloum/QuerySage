
import logging
from flask import Flask
from app.router import register_blueprints

def create_app():
    app = Flask(__name__)

    # 错误捕获
    @app.errorhandler(404)
    def page_not_found(error):
        return 'not found', 404
    
    config_logging()
    
    # 注册蓝图
    register_blueprints(app)

    return app

# 日志配置
def config_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
