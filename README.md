📚 Internal Docs RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot deployed on AWS Lambda using Docker container images, designed to answer questions from internal documents efficiently and cost-effectively.

Built with FastAPI + FAISS + HuggingFace Embeddings, following serverless and cloud-native best practices.

🚀 Key Highlights

Serverless-first architecture using AWS Lambda (Container Image)

Dockerized FastAPI application, Lambda-compatible

RAG pipeline with document ingestion, chunking, embeddings, and vector search

Mock LLM mode for zero-cost development & CI testing

Clean, modular codebase following backend best practices

🧠 System Architecture (High Level)
Client → FastAPI (Lambda) → Retriever (FAISS) → LLM (Local / Mock)


Documents are ingested and indexed into a FAISS vector store

Queries retrieve top-K relevant chunks

Context is passed to an LLM (local or mock) to generate answers

📁 Project Structure
internal-docs-rag-chatbot/
├── src/
│   ├── app.py          # FastAPI entry point (Lambda handler via Mangum)
│   ├── ingest.py       # Document ingestion & vector indexing
│   ├── chat_local.py   # Local LLM inference
│   ├── chat_mock.py    # Mock LLM for testing / no-cost mode
│   ├── config.py       # Environment-based configuration
│   └── aws/            # AWS-specific helpers
│
├── data/               # Source documents
├── Dockerfile          # Lambda-compatible Docker image
├── requirements.txt
├── requirements-lambda.txt
├── test_fastapi.py     # Basic API tests
└── README.md

⚙️ Tech Stack

Backend: FastAPI, Python 3.10+

RAG: FAISS, HuggingFace Embeddings

Deployment: AWS Lambda (Container Image), Amazon ECR

DevOps: Docker, AWS CLI

Testing: Pytest / FastAPI TestClient

🐳 Run Locally with Docker (Lambda Runtime)
docker build -t rag-chatbot-lambda .
docker run --rm -p 9000:8080 rag-chatbot-lambda


Invoke locally (Lambda-style):

curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -H "Content-Type: application/json" \
  -d '{"httpMethod":"GET","path":"/health"}'

☁️ AWS Deployment (Summary)

Build Lambda-compatible Docker image

Push image to Amazon ECR

Create AWS Lambda function (Image type)

Optional: expose via Lambda Function URL

✔ Successfully deployed and tested on AWS Lambda.

🧪 Development Mode

chat_mock.py allows running the full RAG flow without calling external LLM APIs

Ideal for:

CI/CD

Cost-free demos

Local testing

🎯 Why This Project Matters

This project demonstrates:

Real-world RAG system design

Practical serverless & Docker deployment

Awareness of cost optimization (Mock LLM)

Clean separation between ingestion, retrieval, and generation

👤 Author

Hoàng Tuyến