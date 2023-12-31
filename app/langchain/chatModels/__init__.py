
import logging
from typing import Dict,List
from langchain_core.documents import Document
from langchain.chains import LLMChain, StuffDocumentsChain
from langchain.document_transformers import (
    LongContextReorder,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

from config import OPEN_AI_MODEL, OPEN_BASE_URL, OPEN_AI_TOKEN, OPEN_AI_PROXY,OPEN_AI_ORGANIZATION


class ChatClass():
    def start(self, query: str, documents: List[Document]):
        document_prompt,prompt,document_variable_name = self.created_template()

        llm = self.open_ai()

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )

        with get_openai_callback() as tokens:
            chat_data = chain.run(input_documents=documents, query=query)
            logging.info(tokens)
          
        return chat_data

    def open_ai(self)->ChatOpenAI:
        return ChatOpenAI(
                model_name=OPEN_AI_MODEL,
                openai_api_base=OPEN_BASE_URL,
                openai_api_key=OPEN_AI_TOKEN,
                openai_organization=OPEN_AI_ORGANIZATION,
                temperature=0.5,
                request_timeout=60000,
            )
    

    def created_template(self):
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )
        stuff_prompt_override = """Given this content:
        -----
        {context}
        -----
        Please answer the following question:
        {query}"""
        prompt = PromptTemplate(
            template=stuff_prompt_override, input_variables=["context", "query"]
        )

        document_variable_name = "context"

        return document_prompt,prompt,document_variable_name

Chat = ChatClass()