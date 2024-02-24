from fastapi import Depends, FastAPI

from app.langchain.chat.chat_agent import agent_chat
from app.utils.verify_token import verify_token

def chat_routes(app: FastAPI):

    app.post("/chat/agent_chat",
             dependencies=[Depends(verify_token)],
             tags=["Chat"],
             summary="与agent对话")(agent_chat)
    