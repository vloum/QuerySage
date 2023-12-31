
from typing import List
import jieba
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.documents import Document

class SplitterClass(object):
    splitter: RecursiveCharacterTextSplitter

    def __init__(self) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )
        pass
    
    # 分词
    def split_word(self, query: str = '') -> List[str]:
        seg_list = jieba.cut(query, cut_all=False)  # 精确模式
        seg_list = list(seg_list)
        return seg_list
    
    def split_documents(self, documents: List[Document])->List[Document]:
        path = documents[0].metadata.get('source', '')
        if path:
          if 'md' in path.split('.')[-1].lower():
              documents = self.md_split_documents(documents=documents)

        return self.splitter.split_documents(documents=documents)
    
    # md split
    def md_split_documents(self, documents: List[Document]) -> List[Document]:
        headers_to_split_on = [
            ("#", "Header1"),
            ("##", "Header2"),
            ("###", "Header3"),
            ("####", "Header4"),
        ]

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_content = '\n'.join([doc.page_content for doc in documents])
        md_header_splits = markdown_splitter.split_text(md_content)

        return md_header_splits
    
Splitter = SplitterClass()