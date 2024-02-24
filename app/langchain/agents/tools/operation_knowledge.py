import json
from pydantic import BaseModel, Field
from typing import Dict, Optional
from langchain.docstore.document import Document
from langchain.chains.openai_functions import convert_to_openai_function
from app.langchain.chat import Chat

from config import SU_KNOWLEDGE_URL, SU_KNOWLEDGE_KEY, SU_KNOWLEDGE_TABLE, SU_KNOWLEDGE_MATCH_FUNCTION

from app.langchain.vector.supabase import InitSu
from app.utils.verify_token import parse_agent_token, remove_agent_token, token_var

# 初始化 subapase

Knowledge_db = InitSu({
    'url': SU_KNOWLEDGE_URL,
    'service_key': SU_KNOWLEDGE_KEY,
    'table_name': SU_KNOWLEDGE_TABLE,
    'query_name': SU_KNOWLEDGE_MATCH_FUNCTION
})

save_types = [
    { 'type': 'life', 'description': '生活相关或个人信息' },
    { 'type': 'file', 'description': '文件' },
    { 'type': 'image', 'description': '图片' },
    { 'type': 'other', 'description': '其他' }
]


def save_knowledge(query: str):
    try:
        new_query = chat_save_data(query)
        file_data = new_query.get('file_data', {})
        save_type = new_query.get('save_type', 'other')
        # 如果存在 id 
        file_id = file_data.get('file_id', '')
        file_description = file_data.get('file_description', '')

        documents = create_documents(query=query, file_id=file_id, file_description=file_description, type=save_type)

        # 存储文档
        Knowledge_db.form_documents(documents)
        return '存储成功'
    except Exception as e:
        return '存储失败，请告知并结束对话'

def create_documents(query: str, file_id: str, file_description: str, type: str) -> list[Document]:
    documents = []

    token, query = parse_query_to_token_and_query(query)

    if file_id:
        documents.append(Document(
            page_content=file_description,
            metadata={
                'file_id': file_id,
                'user_id': token,
                'type': type
            }
        ))
    else:
        documents.append(Document(
            page_content=query,
            metadata={
                'file_id': file_id,
                'file_description': file_description,
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

        content = '这是知识库相关内容：\n'
        for item in result:
            doc = item[0]
            content += f"{doc.page_content}\n"
        
        return content
    except Exception as e:
        return f'搜索失败，请告知并结束对话，并解释失败原因。原因是：{e}'

def parsing_query_to_json(query: str):
    try:
        return json.loads(query.strip(" "))
    except Exception as e:
        return query

def parse_query_to_token_and_query(query: str):
    token = parse_agent_token(query)
    query = remove_agent_token(query)
    return token, query

class FileData(BaseModel):
    file_id: str = Field(description="File ID")
    file_description: str = Field(description="File Description")

class KnowledgeInput(BaseModel):
    query: str = Field(description="Store according to the original content, if it includes images, the description and address of the image need to be stored")


class KnowledgeSearchInput(BaseModel):
    query: str = Field(description="Knowledge to be searched")
    
    k: Optional[int] = Field(4, description="Top k results to be returned")

class FunctionCall(BaseModel):
    '''获取存储内容所需要的信息'''
    save_type: str = Field(description="just choose one of the following types", enum=[item['type'] for item in save_types])
    file_data: Optional[FileData] = Field({},description="has file data choose file type, if not, return empty object")


function = convert_to_openai_function(FunctionCall)
def chat_save_data(query: str)-> Dict:
    try:
        data = Chat.llm.invoke(query, functions=[function], function_call={"name": "FunctionCall"})

        additional_kwargs = data.additional_kwargs
        return parsing_query_to_json(additional_kwargs['function_call']['arguments'])
    except Exception as e:
        return {'save_type': 'other', 'file_data': {}}
