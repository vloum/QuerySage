
from typing import Any, List
from langchain.docstore.document import Document
from langchain.vectorstores.supabase import SupabaseVectorStore
from supabase.client import Client, create_client
from supabase.lib.client_options import ClientOptions
from app.langchain.embedding import Embedding

from config import SU_URL, SU_SERVICE_KEY,SU_TABLE,SU_MATCH_FUNCTION, SU_TIMEOUT

class InitSu(object):
    client: Client
    vector_store: SupabaseVectorStore
    embedding: Any
    table_name: str = SU_TABLE
    query_name: str = SU_MATCH_FUNCTION
    def __init__(self) -> None:
        self.client : Client = create_client(SU_URL, SU_SERVICE_KEY, ClientOptions(postgrest_client_timeout=SU_TIMEOUT))
        self.embedding = Embedding.beg()
        # 初始化
        self.vector_store = SupabaseVectorStore(
            client=self.client,
            embedding= self.embedding,
            table_name=self.table_name,
            query_name=self.query_name,
            chunk_size=400
        )
        pass
    
    # 模糊查询
    def search_keyword(self, keyword: str):
        list = self.client.from_(self.table_name).select('*').like('content', f'%{keyword}%').limit(20).execute()
        if list:
            return list.data
        return []
    
    # form_documents
    def form_documents(self, documents: List[Document]) -> List:
        return self.vector_store.add_documents(documents=documents)

    def similarity_documents(self, query: str) -> List[Document]:
        return self.vector_store.similarity_search(query=query)

    def similarity_documents_score(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search_with_relevance_scores(query, k=k)
    
    def max_marginal_relevance_search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.max_marginal_relevance_search(query, k=k)

Supabase = InitSu()