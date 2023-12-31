

from typing import List
from langchain.docstore.document import Document
from app.langchain.contentLoader import DocumentLoader
from app.langchain.contentLoader.split_content import Splitter
from app.langchain.embedding import Embedding
from app.langchain.embedding.compute import maximal_marginal_relevance
from app.langchain.vector.supabase import Supabase
from app.utils import process_tasks

# 关于法律文档处理
def process_laws_documents(title: str, files: List[str]) -> bool:
    all_split_documents, documents_contents  = collection_and_split_documents(files=files, title=title)

    # 存入数据库
    Supabase.form_documents(all_split_documents)

    return True

# 根据输入处理文档
def process_documents(query: str, files: List[str])->List[Document]:
    # 收集所有分割好的文档内容
    all_split_documents, documents_contents  = collection_and_split_documents(files=files)

    # 做向量
    chat_documents = computed_similarity_documents(all_split_documents=all_split_documents, documents_contents=documents_contents, query=query)

    return chat_documents

# 切割并收集
def collection_and_split_documents(files: List[str], title: str = ''):
    # 收集所有分割好的文档内容
    documents_contents = []
    all_split_documents = []
    un_support_file = []
    List_documents = DocumentLoader().load_document(files=files)

    for documents in List_documents:
        if isinstance(documents, list):
            split_documents = Splitter.split_documents(documents=documents)
            for doc in split_documents:
                if title:
                    all_split_documents.append(
                      Document(
                          page_content=doc.page_content,
                          metadata={
                              **doc.metadata,
                              'title': title
                          }
                      )
                    )
                else:
                    all_split_documents.append(doc)
                documents_contents.append(doc.page_content)
        else:
            un_support_file.append(documents)
    
    if len(documents_contents) == 0:
        raise ValueError({ 'code': 4006, 'un_support_file': un_support_file, 'message': '缺少支持的 file' })
    
    return all_split_documents, documents_contents
    
# 计算筛选存在一定相关度的文本字段
def computed_similarity_documents(all_split_documents: List[Document],documents_contents: List[str], query: str):
     # 做向量
    embedding_instance = Embedding.beg()
    content_embeddings = embedding_instance.embed_documents(documents_contents)
    query_embedding = embedding_instance.embed_query(query)

    # 计算相关度
    similarities = maximal_marginal_relevance(query_embedding, embedding_list=content_embeddings, lambda_mult=0, k = min(10, len(content_embeddings)))

    chat_documents = [ all_split_documents[similarity[0]] for similarity in similarities if similarity[1] > 0.5]

    return chat_documents

# 结巴分词，然后数据库模糊查询
def jie_ba_and_search_documents(query: str)-> List[Document]:
    word_list = Splitter.split_word(query=query)

    filtered_keywords = [keyword for keyword in word_list if len(keyword) >= 2]
    # 使用 process_tasks 函数并发执行任务
    search_documents = process_tasks(filtered_keywords, Supabase.search_keyword)

    return search_documents
