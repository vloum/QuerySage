from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field
from langchain.llms.openai import OpenAI

from app.langchain.utils import get_ChatOpenAI
from config import OPEN_BASE_URL, OPEN_AI_TOKEN
import os

def dalle_image_generator(query: str):
  os.environ["OPENAI_API_KEY"] =OPEN_AI_TOKEN
  os.environ["OPENAI_API_BASE"] =OPEN_BASE_URL
  llm = OpenAI(
            temperature=0.1
        )

  prompt = PromptTemplate(
      input_variables=["image_desc"],
      template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
  )
  chain = LLMChain(llm=llm, prompt=prompt)

  image_url = DallEAPIWrapper().run(chain.run(query))

  return image_url

class DalleImageGeneratorInput(BaseModel):
    query: str = Field()
