from app.langchain.document_loader.utils import KnowledgeFile, files2docs_in_thread

from fastapi import Depends

from app.utils import upload_files_dependency

def parsing_docs(data = Depends(upload_files_dependency)):
    
    files = data.get('files', None)

    if not files:
        return { 'code': 4006, 'message': '缺少文件' }

    kb_files = [KnowledgeFile(filename=file_data.get('filename'), knowledge_base_name=data.get('knowledge_name')) for file_data in files]
    
    results = files2docs_in_thread(files=kb_files)

    result_content = []
    for item in results:
        docs = item[1][2]
        content = ''
        for doc in docs:
            content+=doc.page_content

        result_content.append({
            'content': content,
            'file': item[1][1]
        })

    return { 'code': 200, 'message': '导入成功', 'result_content': result_content}
