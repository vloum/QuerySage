from langchain.embeddings import HuggingFaceBgeEmbeddings

class EmbeddingStore(object):
    def __init__(self) -> None:
        pass
    
    def beg(self) -> HuggingFaceBgeEmbeddings:
        model_name = "BAAI/bge-small-en"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        return HuggingFaceBgeEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
        )


Embedding = EmbeddingStore()