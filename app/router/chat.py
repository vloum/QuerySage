from app.langchain.chat.chat_agent import agent_chat

from fastapi import FastAPI


def chat_routes(app: FastAPI):
    app.post("/chat/agent_chat",
             tags=["Chat"],
             summary="与agent对话")(agent_chat)

