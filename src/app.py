from fastapi import FastAPI
from pydantic import BaseModel

try:
    from mangum import Mangum
    USE_LAMBDA = True
except ImportError:
    USE_LAMBDA = False

from chat_mock import get_chat_response

# ==============================
# FastAPI App
# ==============================
app = FastAPI(
    title="Internal Docs RAG Chatbot",
    description="Serverless RAG chatbot for internal documents",
    version="1.0.0"
)

# ==============================
# Lambda handler
# ==============================
if USE_LAMBDA:
    handler = Mangum(app, lifespan="off")

# ==============================
# Request Schema
# ==============================
class ChatRequest(BaseModel):
    question: str

# ==============================
# Chat Endpoint
# ==============================
@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    Chat endpoint for RAG chatbot.
    Currently uses mock LLM.
    Can be replaced with real RAG pipeline without changing API contract.
    """
    return get_chat_response(req.question)

# ==============================
# Health Check
# ==============================
@app.get("/health")
def health_check():
    return {"status": "ok"}
