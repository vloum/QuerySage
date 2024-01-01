

from app.controller.documents import keyword_search_documents
from app.langchain.chatModels import Chat
from app.langchain.embedding import Embedding
from app.langchain.embedding.compute import maximal_marginal_relevance
from langchain.docstore.document import Document

class ChatClass(object):

    # 法律问答
    @staticmethod
    def law(query: str):
        keyword_lists =  Chat.chat_split_word(query)
        # 分词检索 , 这里查询出来的是数据库的数据结构
        search_documents = keyword_search_documents(word_list=keyword_lists)

        documents = []
        document_embeddings = [] # use embedding
        chat_documents = [] # use chat
        for lists in search_documents:
            if len(lists) > 0:
                documents+=lists
        
        is_had = []
        for doc in documents:
            doc_item = doc[0]
            if not doc_item.page_content in is_had:
                document_embeddings.append(doc[2])
                chat_documents.append(
                    Document(
                        page_content= doc_item.page_content,
                        metadata=doc_item.metadata
                    )
                )

                is_had.append(doc_item.page_content)

        query_embedding = Embedding.embed_query(text=query)

        similarity_lists = maximal_marginal_relevance(query_embedding=query_embedding, embedding_list=document_embeddings, lambda_mult=0, k=len(document_embeddings))

        sorted_similarities = sorted(similarity_lists, key=lambda x: x[1], reverse=True)

        # 选取相似度大于 0.8 的前四个文档
        docs = [chat_documents[sim[0]] for sim in sorted_similarities if sim[1] > 0.8][:4]

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
