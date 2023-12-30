from flask import Blueprint
from app.controller.documents import process_documents
from app.utils import post_data

document_blueprint = Blueprint('document', __name__)

@document_blueprint.route('/', methods=['GET'])
def hello_world_embedding():
    return "<p>Hello, World embedding!</p>"

@document_blueprint.route('/query', methods=['POST'])
def docs_query():
    body = post_data()

    files = body.get('files', None)
    query = body.get('query', '')

    if not query or not files:
        return { 'code': 4006, 'message': '缺少必要参数 query or files' }

    documents = process_documents(query=query, files=files)

    return { 'code': 200 }, 200