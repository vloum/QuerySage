from app.langchain.chat.chat_agent import agent_chat

from fastapi import FastAPI


def chat_routes(app: FastAPI):
    app.post("/chat/agent_chat",
             tags=["Chat"],
             summary="与agent对话")(agent_chat)
    

# class AgentChatRequest(BaseModel):
#     query: str
#     history: List[Any] = []
#     stream: bool = False
#     model_name: str = 'default'
#     temperature: float = 0.7
#     max_tokens: Optional[int] = None
#     prompt_name: str = 'default'

# @chat_router.post('/laws')
# def query_laws(query: str = Body(..., description="查询内容")):
#     if not query:
#         raise HTTPException(status_code=400, detail="缺少必要参数 query or files")

#     result = ControllerChat.law(query=query)
#     return {'code': 200, 'data': result}
