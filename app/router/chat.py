from flask import Blueprint
from app.controller.chat import ControllerChat

chat_blueprint = Blueprint('chat', __name__)
from app.utils import post_data

@chat_blueprint.route('/laws', methods=['POST'])
def query_laws():
    body = post_data()

    query = body.get('query', '')

    if not query:
        return { 'code': 4006, 'message': '缺少必要参数 query or files' }
    

    result = ControllerChat.law(query=query)

    return { 'code': 200, 'data': result }


