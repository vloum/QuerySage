from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field

from config import OPEN_BASE_URL, OPEN_AI_TOKEN

def dalle_image_generator(query: str):
  image_url = DallEAPIWrapper(api_key=OPEN_AI_TOKEN, base_url=OPEN_BASE_URL, model='dall-e-3').run(query=query)

  return image_url

class DalleImageGeneratorInput(BaseModel):
    query: str = Field()
