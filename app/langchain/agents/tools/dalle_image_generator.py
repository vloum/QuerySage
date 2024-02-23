import uuid
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import BaseModel, Field
from app.utils.tencent_cos import cos_upload_file

from config import OPEN_BASE_URL, OPEN_AI_TOKEN, OPEN_AI_DALLE_URL

OPEN_AI_DALLe_BASE_URL = 'https://oaidalleapiprodscus.blob.core.windows.net'

def dalle_image_generator(query: str):
   image_url = DallEAPIWrapper(
         model='dall-e-3',
         api_key=OPEN_AI_TOKEN,
         base_url=OPEN_BASE_URL,
         max_retries=1,
      ).run(query=query)
   
   if OPEN_AI_DALLe_BASE_URL in image_url and OPEN_AI_DALLE_URL:
      image_url = image_url.replace(OPEN_AI_DALLe_BASE_URL, OPEN_AI_DALLE_URL)

   file_id = str(uuid.uuid4())
   # 存到对象桶里
   image_url = cos_upload_file(image_url, file_id)

   # 转成md格式
   return f'![{query}]({image_url})'

class DalleImageGeneratorInput(BaseModel):
    query: str = Field()
