from fastapi import FastAPI
from pydantic import BaseModel

try:
    from mangum import Mangum
    USE_LAMBDA = True
except ImportError:
    USE_LAMBDA = False

from src.chat_mock import get_chat_response

app = FastAPI(
    title="Internal Docs RAG Chatbot",
    description="Mock RAG chatbot for serverless deployment",
    version="1.0.0"
)

if USE_LAMBDA:
    handler = Mangum(app)  # AWS Lambda entrypoint

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return get_chat_response(req.query)

@app.get("/health")
def health_check():
    return {"status": "ok"}
