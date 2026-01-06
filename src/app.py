from fastapi import FastAPI
from pydantic import BaseModel

from src.chat_mock import get_chat_response

app = FastAPI(
    title="Internal Docs RAG Chatbot",
    description="Mock RAG chatbot for serverless deployment",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return get_chat_response(req.query)


@app.get("/health")
def health_check():
    return {"status": "ok"}
