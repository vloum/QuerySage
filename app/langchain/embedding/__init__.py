from typing import Any, List, Optional, Union

from langchain.embeddings import HuggingFaceBgeEmbeddings, OpenAIEmbeddings

from config import EMBEDDING_TYPE, OPEN_BASE_URL, OPEN_AI_TOKEN, OPEN_AI_PROXY, OPEN_AI_ORGANIZATION

class EmbeddingStore(object):
    embedding: Optional[Union[OpenAIEmbeddings, HuggingFaceBgeEmbeddings]] = None
    def __init__(self) -> None:
        if EMBEDDING_TYPE == 'open_ai':
            self.embedding = self.open_ai()
        else:
            self.embedding = self.beg()
        pass
    
    def beg(self) -> HuggingFaceBgeEmbeddings:
        model_name = "BAAI/bge-small-en"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        return HuggingFaceBgeEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        )
    
    def open_ai() -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            base_url=OPEN_BASE_URL,
            api_key=OPEN_AI_TOKEN,
            openai_proxy=OPEN_AI_PROXY,
            organization=OPEN_AI_ORGANIZATION,
        )


Embedding = EmbeddingStore().embedding