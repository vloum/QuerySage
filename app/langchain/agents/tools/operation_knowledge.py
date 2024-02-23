from pydantic import BaseModel, Field
from typing import Optional
from langchain.docstore.document import Document

from config import SU_KNOWLEDGE_URL, SU_KNOWLEDGE_KEY, SU_KNOWLEDGE_TABLE, SU_KNOWLEDGE_MATCH_FUNCTION

from app.langchain.vector.supabase import InitSu

# 初始化 subapase

Knowledge_db = InitSu({
    'url': SU_KNOWLEDGE_URL,
    'service_key': SU_KNOWLEDGE_KEY,
    'table_name': SU_KNOWLEDGE_TABLE,
    'query_name': SU_KNOWLEDGE_MATCH_FUNCTION
})


def operation_knowledge(query: str, file_id: str, file_description: str):
    # 如果存在 id 

    documents = create_documents(query=query, file_id=file_id, file_description=file_description)

    # 存储文档
    return Knowledge_db.form_documents(documents)


def create_documents(query: str, file_id: str, file_description: str) -> list[Document]:
    documents = []

    documents.append(Document(
        page_content=query,
        metadata={
            'file_id': file_id,
            'file_description': file_description
        }
    ))

    return documents


class FileData(BaseModel):
    file_id: str = Field(description="File ID")
    file_description: str = Field(description="File Description")

class KnowledgeInput(BaseModel):
    query: str = Field(description="Knowledge to be stored")
    file_data: Optional[FileData] = Field(description="File Data (optional)")