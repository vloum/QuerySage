# from flask import Blueprint, render_template
# from app.controller.documents import process_documents, process_laws_documents
# from app.langchain.chat import Chat
# from app.langchain.document_loader.utils import KnowledgeFile, files2docs_in_thread
# from app.utils import post_data

# document_blueprint = Blueprint('document', __name__)

# @document_blueprint.route('/', methods=['GET'])
# def hello_world_embedding():
#     return "<p>Hello, World embedding!</p>"

# @document_blueprint.route('/query', methods=['POST'])
# def docs_query():
#     body = post_data()

#     files = body.get('files', None)
#     query = body.get('query', '')

#     if not query or not files:
#         return { 'code': 4006, 'message': '缺少必要参数 query or files' }

#     documents = process_documents(query=query, files=files)

#     chat_data = Chat.start(query=query, documents=documents)

#     return { 'code': 200, 'result': chat_data}, 200


# @document_blueprint.route('/laws', methods=['POST'])
# def import_laws():
#     body = post_data()

#     files = body.get('files', None)
#     title = body.get('title', '')

#     if not files:
#         return { 'code': 4006, 'message': '缺少必要法律文件' }

#     kb_files = [KnowledgeFile(filename=file_data.get('filename'), knowledge_base_name=body.get('knowledge_name')) for file_data in files]
    
#     # result = process_laws_documents(title=title, files=files)

#     results = files2docs_in_thread(files=kb_files)

#     result_content = []
#     for item in results:
#         docs = item[1][2]
#         content = ''
#         for doc in docs:
#             content+=doc.page_content

#         result_content.append({
#             'content': content,
#             'file': item[1][1]
#         })

#     return { 'code': 200, 'message': '导入成功', 'result_content': result_content}

# @document_blueprint.route('/upload', methods=['GET'])
# def upload_laws():
#     return render_template('/templates/law.html', title='法律文件上传')