import re
import json
from pydantic import BaseModel, Field
from typing import Dict, Optional
from langchain.docstore.document import Document
from langchain.chains.openai_functions import convert_to_openai_function
from langchain.chat_models import ChatOpenAI
from app.langchain.chat import Chat
from app.utils.backend_ability import get_cache_by_backend
from app.utils.tencent_cos import BASEURL

from config import OPEN_AI_ORGANIZATION, OPEN_AI_TOKEN, OPEN_BASE_URL, SU_KNOWLEDGE_URL, SU_KNOWLEDGE_KEY, SU_KNOWLEDGE_TABLE, SU_KNOWLEDGE_MATCH_FUNCTION

from app.langchain.vector.supabase import InitSu
from app.utils.verify_token import parse_agent_token, remove_agent_token, token_var

# 初始化 subapase

Knowledge_db = InitSu({
    'url': SU_KNOWLEDGE_URL,
    'service_key': SU_KNOWLEDGE_KEY,
    'table_name': SU_KNOWLEDGE_TABLE,
    'query_name': SU_KNOWLEDGE_MATCH_FUNCTION
})

SAVE_TYPE = [
    { 'type': 'life', 'description': '生活相关或个人信息' },
    { 'type': 'file', 'description': '文件' },
    { 'type': 'image', 'description': '图片' },
    { 'type': 'other', 'description': '其他' }
]

FILE_TYPES = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt']
IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'svg']


class FileData(BaseModel):
    file_id: str = Field(description="File ID")
    isTrue: Optional[bool] = Field(description="根据输入条件判断是否需要全文或者只需要检索文件部分内容")
    # 文件后缀
    file_suffix: Optional[str] = Field(description="File suffix")

class KnowledgeInput(BaseModel):
    query: str = Field(description="Store according to the original content, if it includes images, the description and address of the image need to be stored")


class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="Knowledge to be searched.if it includes file or image,please input include file_id or image_id.")
    
    k: Optional[int] = Field(4, description="Top k results to be returned")

class FunctionCall(BaseModel):
    '''获取存储内容所需要的信息'''
    save_type: str = Field(description="just choose one of the following types", enum=[item['type'] for item in SAVE_TYPE])
    file_data: Optional[FileData] = Field({},description="has file data choose file type, if not, return empty object")

function = convert_to_openai_function(FunctionCall)

big_file_chat = ChatOpenAI(
            model_name='gpt-4-0125-preview', # 128k
            openai_api_base=OPEN_BASE_URL,
            openai_api_key=OPEN_AI_TOKEN,
            openai_organization=OPEN_AI_ORGANIZATION,
            temperature=0.5,
            request_timeout=60000,
        )

# 大文件问答
def query_big_file(query: str, file_id: str):
    try:
        file_content = get_cache_by_backend(file_id)

        prompt = '''
            问题输入是：{query}\n
            内容是：\n{file_content}
            请回答
        '''
        query = prompt.format(query=query, file_content=file_content)

        data = big_file_chat.llm.invoke(query)
        return '这是数据库文件问答的结果：\n' + data.content
    except Exception as e:
        return '大文件问答失败'

def save_knowledge(query: str):
    try:
        new_query = chat_save_data(query)
        file_data = new_query.get('file_data', {})
        save_type = new_query.get('save_type', 'other')
        # 如果存在 id 
        file_id = file_data.get('file_id', '')
        file_suffix = file_data.get('file_suffix', '')

        documents = create_documents(query=query, file_id=file_id, file_suffix=file_suffix, type=save_type)

        # 存储文档
        Knowledge_db.form_documents(documents)
        return '存储成功'
    except Exception as e:
        return '存储失败，请告知并结束对话'

def create_documents(query: str, file_id: str,file_suffix: str, type: str) -> list[Document]:
    documents = []

    token, query = parse_query_to_token_and_query(query)

    if file_id:
        file_description = get_file_info(file_id, file_suffix)
        documents.append(Document(
            page_content=file_description,
            metadata={
                'file_id': file_id,
                'user_id': token,
                'file_suffix': file_suffix,
                'type': type
            }
        ))
    else:
        documents.append(Document(
            page_content=query,
            metadata={
                'user_id': token,
                'type': type
            }
        ))

    return documents

def search_knowledge(query: str, k: int = 4):
    try:
        token, query = parse_query_to_token_and_query(query)

        search_data = chat_save_data(query)

        filter = {
            'user_id': token,
            'type': search_data.get('save_type', 'other')
        }
        # 搜索文档
        result = Knowledge_db.similarity_documents_score(query, k, filter=filter)

        if len(result) == 0:
            return '知识库没有相关内容'

        content = '这是知识库找到的信息：\n'

        for item in result:
            doc = item[0]
            file_id = doc.metadata.get('file_id','')
            ext = doc.metadata.get('file_suffix','')
            file_path = f'{BASEURL}{file_id}.{ext}'
            if filter.get('type') == 'image':
                content += f"![{doc.page_content}]({file_path})\n"
            elif ext in FILE_TYPES:
                content += f"[该文件]({file_path}):\n 文件简介：```text \n{doc.page_content}\n```\n"
            else:
                content += f"{doc.page_content}\n"

        return content
    except Exception as e:
        return f'知识库没找到内容，解释失败原因。原因是：{e}'

def parsing_query_to_json(query: str):
    try:
        return json.loads(query.strip(" "))
    except Exception as e:
        return query

def parse_query_to_token_and_query(query: str):
    token = parse_agent_token(query)
    query = remove_agent_token(query)
    return token, query


def chat_save_data(query: str)-> Dict:
    try:
        data = Chat.llm.invoke(query, functions=[function], function_call={"name": "FunctionCall"})

        additional_kwargs = data.additional_kwargs
        print('additional_kwargs:', additional_kwargs)
        call_data = parsing_query_to_json(additional_kwargs['function_call']['arguments'])

        if call_data.get('file_data', {}).get('file_id', ''):
            call_data['file_data']['file_id'] = parsing_file_id(call_data['file_data']['file_id'])

        return call_data
    except Exception as e:
        return {'save_type': 'other', 'file_data': {}}

# 查询文件并概括文件信息存储
def get_file_info(file_id: str, file_suffix: str) -> str:
    try:
        file_content = get_cache_by_backend(file_id)
        # 如果是图片可以直接返回
        if file_suffix in IMAGE_TYPES:
            return file_content
        # 如果是文件，需要简述文件内容
        if file_suffix in FILE_TYPES:
            file_content = file_content[:1000]
            # 写个prompt用于模型简述文件内容用于存储
            query = f'简述文件内容：{file_content}'
            data = Chat.llm.invoke(query)
            return data.content
        return file_content
    except Exception as e:
        raise  ValueError(f'{e}')

def parsing_file_id(file_id: str) -> str:
    id = re.compile(r'([a-zA-Z\d]+(?:[-][a-zA-Z\d]{4}){3}-[a-zA-Z\d]+)').search(file_id)
    if not id:
        return ''
    return id.group(1)
