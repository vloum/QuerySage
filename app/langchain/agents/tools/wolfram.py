# Langchain 自带的 Wolfram Alpha API 封装
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from pydantic import BaseModel, Field
from config import WOLFRAM_APP_ID
wolfram_alpha_appid = WOLFRAM_APP_ID
def wolfram(query: str):
    wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid=wolfram_alpha_appid)
    ans = wolfram.run(query)
    return ans

class WolframInput(BaseModel):
    location: str = Field(description="需要运算的具体问题")