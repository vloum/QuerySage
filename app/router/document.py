from app.langchain.document_loader.utils import KnowledgeFile, files2docs_in_thread

from fastapi import Depends

from app.utils import get_md_format, upload_files_dependency
from app.utils.backend_ability import get_cache_by_backend, save_cache_by_backend
from app.utils.tencent_cos import BUCKET, REGION

def parsing_docs(data = Depends(upload_files_dependency)):
    
    files = data.get('files', None)

    if not files:
        return { 'code': 4006, 'message': '缺少文件' }

    kb_files = [KnowledgeFile(filename=file_data.get('filename'), knowledge_base_name=data.get('knowledge_name')) for file_data in files]

    results = files2docs_in_thread(files=kb_files)

    result_content = []
    for index, item in enumerate(results):
        docs = item[1][2]
        content = ''
        splitter = []
        if isinstance(docs, list):
            for doc in docs:
                # splitter.append(doc.page_content)
                content+=doc.page_content
        else:
            content = docs
        file_name = item[1][1]
        url = f'https://{BUCKET}.cos.{REGION}.myqcloud.com/{file_name}'
        origin_name = files[index].get('origin_name', '')

        result_content.append({
            'content': content,
            'splitter': splitter,
            'file_name': file_name,
            'utl': url,
            'md': get_md_format(origin_name.split('.')[-1], url, content, origin_name)
        })
        # 存入数据库
        key = file_name.split('.')[0]
        save_cache_by_backend(key, content)
    

    return { 'code': 200, 'message': '导入成功', 'files': result_content}
