

from typing import List
from langchain_core.documents import Document
from app.langchain.contentLoader import DocumentLoader
from app.langchain.contentLoader.split_content import Splitter
from app.langchain.embedding import Embedding
from app.langchain.embedding.compute import maximal_marginal_relevance


def process_documents(query: str, files: List[str])->List[Document]:
    # 收集所有分割好的文档内容
    documents_contents = []
    all_split_documents = []
    un_support_file = []
    List_documents = DocumentLoader().load_document(files=files)

    for documents in List_documents:
        if isinstance(documents, list):
            split_documents = Splitter.split_documents(documents=documents)
            for doc in split_documents:
                all_split_documents.append(doc)
                documents_contents.append(doc.page_content)
        else:
            un_support_file.append(documents)
    
    if len(documents_contents) == 0:
        raise ValueError({ 'code': 4006, 'un_support_file': un_support_file, 'message': '缺少支持的 file' })

    # 做向量
    embedding_instance = Embedding.beg()
    content_embeddings = embedding_instance.embed_documents(documents_contents)
    query_embedding = embedding_instance.embed_query(query)

    # 计算相关度
    similarities = maximal_marginal_relevance(query_embedding, embedding_list=content_embeddings, lambda_mult=0, k = min(10, len(content_embeddings)))

    chat_documents = [ all_split_documents[similarity[0]] for similarity in similarities]

    return chat_documents