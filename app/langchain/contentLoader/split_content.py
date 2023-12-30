
from typing import Iterable, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
    
    def split_documents(self, documents: List[Document])->List[Document]:
        return self.splitter.split_documents(documents=documents)
    
Splitter = SplitterClass()