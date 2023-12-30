from typing import Any, Dict, List, Callable, List, Tuple
import concurrent.futures

from langchain_core.documents import Document
from langchain.document_loaders import BiliBiliLoader, CSVLoader, DocusaurusLoader, UnstructuredExcelLoader, UnstructuredImageLoader, UnstructuredPowerPointLoader, Docx2txtLoader, WikipediaLoader, PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader

class DocumentLoader(object):
    def __init__(self, body: Dict[Any]) -> None:
        pass
    
    def load_document(self, files: List[Dict]) -> List[Document]:
        documents = []
        tasks = []

        for file_info in files:
            file_path = file_info['file_path']
            file_extension = file_path.split('.')[-1].lower()
            task = (self.get_loader(file_extension), file_path)
            tasks.append(task)

        documents = self.execute_concurrently(tasks)

        return documents

    def get_loader(self, file_extension: str) -> Callable:
        # 返回与文件扩展名对应的加载器方法
        loaders = {
            'csv': self.csv,
            'xlsx': self.excel,
            'xls': self.excel,
            'png': self.image,
            'jpg': self.image,
            'jpeg': self.image,
            'ppt': self.ppt,
            'pptx': self.ppt,
            'doc': self.doc,
            'docx': self.docx,
            'pdf': self.pdf,
            'txt': self.txt,
            'md': self.txt
        }
        return loaders.get(file_extension, lambda x: ValueError("Unsupported file type"))

    def execute_concurrently(self, tasks: List[Tuple[Callable, str]]) -> List[Any]:
        # 使用线程池并发执行任务
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(task[0], task[1]) for task in tasks]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results
    
    # 网站视频内容加载
    @staticmethod
    def bilibili(urls: List[str]) -> List[Document]:
        # ["https://www.bilibili.com/video/BV1xt411o7Xu/"]
        loader = BiliBiliLoader(urls)
        return loader.load()
    
    # 网页主要内容获取
    @staticmethod
    def web_loader(url: str) -> List[Document]:
        return DocusaurusLoader(url=url).load()
    
    # csv文件加载
    @staticmethod
    def csv(file_path: str) -> List[Document]:
        loader = CSVLoader(file_path=file_path)

        return loader.load()
    
    # .xlsx and .xls files
    @staticmethod
    def excel(file_path: str) -> List[Document]:
        loader = UnstructuredExcelLoader(file_path)
        return loader.load()
    
    # 加载图片
    @staticmethod
    def image(file_path: str) -> List[Document]:
        return UnstructuredImageLoader(file_path, mode="elements").load()
    
    # 加载ppt
    @staticmethod
    def ppt(file_path: str) -> List[Document]:
        return UnstructuredPowerPointLoader(file_path).load()
    
    # 加载docx
    @staticmethod
    def docx(file_path: str) -> List[Document]:
        return Docx2txtLoader(file_path).load()
    # doc
    @staticmethod
    def doc(file_path: str) -> List[Document]:
        return UnstructuredWordDocumentLoader(file_path).load()
    
    # wiki百科
    @staticmethod
    def wiki(query: str) -> List[Document]:
        return WikipediaLoader(query=query, lang='zh', load_max_docs=5).load()
    
    # pdf文件
    @staticmethod
    def pdf(file_path: str) -> List[Document]:
        return PyPDFLoader(file_path).load()
    
    # md、txt
    @staticmethod
    def txt(file_path: str) -> List[Document]:
        return TextLoader(file_path).load()
