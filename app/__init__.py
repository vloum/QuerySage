
import logging
import traceback
from flask import Flask, jsonify
from app.router import register_blueprints

def create_app():
    app = Flask(__name__)

    # 错误捕获
    @app.errorhandler(404)
    def page_not_found(error):
        return 'not found', 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        # 获取异常的详细信息
        error_info = traceback.format_exc()

        # 为所有其他异常类型设置一个通用的错误响应
        response = {
            "error": str(error),
            "message": "An internal error occurred. Please try again later."
        }
        # 记录异常信息到日志
        logging.error(f"Error: {error}\nDetails: {error_info}")

        return jsonify(response), 500
    
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
