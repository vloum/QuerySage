import logging
from typing import List
from langchain_core.documents import Document
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.document_transformers import LongContextReorder
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

from config import OPEN_AI_MODEL, OPEN_BASE_URL, OPEN_AI_TOKEN, OPEN_AI_PROXY, OPEN_AI_ORGANIZATION


class ChatClass:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=OPEN_AI_MODEL,
            openai_api_base=OPEN_BASE_URL,
            openai_api_key=OPEN_AI_TOKEN,
            openai_organization=OPEN_AI_ORGANIZATION,
            temperature=0.5,
            request_timeout=60000,
        )

    def process_query(self, query: str, documents: List[Document], prompt_template: str):
        document_prompt, document_variable_name = self.create_document_template()
        prompt = self.create_prompt_template(prompt_template)

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )

        with get_openai_callback() as tokens:
            chat_data = chain.run(input_documents=documents, query=query)
            logging.info(tokens)

        return chat_data

    def create_document_template(self):
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )
        document_variable_name = "context"
        return document_prompt, document_variable_name

    def create_prompt_template(self, prompt_override: str):
        return PromptTemplate(
            template=prompt_override, input_variables=["context", "query"]
        )

    def law(self, query: str, documents: List[Document]):
        prompt_template = """
        Considering the legal context provided:
        -----
        {context}
        -----
        This legal question arises:
        {query}
        ---
        Note: Answer in Chinese, providing an in-depth legal analysis and specific advice based on the context. Also, integrate empathy and understanding of the individual's situation, offering not just legal options but also guidance on emotional support and practical steps."""
        return self.process_query(query, documents, prompt_template)

    def start(self, query: str, documents: List[Document]):
        prompt_template = """Given this text extracts:
        -----
        {context}
        -----
        Note: Answer in Chinese.
        Please answer the following question:
        {query}"""
        return self.process_query(query, documents, prompt_template)


Chat = ChatClass()
