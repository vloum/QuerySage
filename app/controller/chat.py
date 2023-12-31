

import numpy as np
from app.controller.documents import jie_ba_and_search_documents
from app.langchain.chatModels import Chat
from app.langchain.embedding import Embedding
from app.langchain.embedding.compute import maximal_marginal_relevance
from app.langchain.vector.supabase import Supabase
from langchain.docstore.document import Document

class ChatClass(object):

    # 法律问答
    @staticmethod
    def law(query: str):
        # 分词检索 , 这里查询出来的是数据库的数据结构
        search_documents = jie_ba_and_search_documents(query=query)

        documents = []
        document_embeddings = [] # use embedding
        chat_documents = [] # use chat
        for lists in search_documents:
            if len(lists) > 0:
                documents+=lists
        

        for doc in documents:
            document_embeddings.append(np.fromstring(
                    doc.get('embedding', "").strip("[]"), np.float32, sep=","
                ))
            chat_documents.append(
                Document(
                    page_content=doc.get('content'),
                    metadata=doc.get('metadata')
                )
            )

        query_embedding = Embedding.beg().embed_query(text=query)

        similarity_lists = maximal_marginal_relevance(query_embedding=query_embedding, embedding_list=document_embeddings, lambda_mult=0, k=len(document_embeddings))


        # 筛选
        docs = []
        for similarity in similarity_lists:
            if similarity[1] > 0.8 and len(docs) < 4:
                docs.append(chat_documents[similarity[0]])


        if len(docs) <= 0:
            docs = Supabase.max_marginal_relevance_search(query=query, k = 2)

        laws = []
        result = Chat.law(query=query, documents=docs)

        for document in docs:
            # 使用列表推导式和join来构建标题
            title_parts = [document.metadata.get(f'Header{i}', '') for i in range(6)]
            title = '-'.join(filter(None, title_parts))  # 过滤掉空字符串

            laws.append({
                'title': title,
                'law': document.page_content
            })

        return { 'result': result, 'laws': laws}


ControllerChat = ChatClass()
