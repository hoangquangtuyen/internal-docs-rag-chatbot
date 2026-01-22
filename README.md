# 📚 Internal Docs RAG Chatbot

A serverless **Retrieval-Augmented Generation (RAG)** chatbot deployed on **AWS Lambda using Docker container images**, designed to answer questions from internal documents efficiently and cost-effectively.

Built with **FastAPI + FAISS + LangChain**, focusing on clean architecture, serverless deployment, and real-world backend practices.

---

## 🚀 Key Features

- Serverless deployment using **AWS Lambda (Container Image)**
- Public **REST API** exposed via **Amazon API Gateway**
- Dockerized **FastAPI** application (Lambda-compatible)
- **Full RAG pipeline implemented using LangChain**: document ingestion, text chunking, embedding generation, and FAISS-based vector search
- **Mock LLM mode** for local testing and cost-free development
- Simple, maintainable backend structure (no unnecessary complexity)

---

## 🧠 Architecture Overview

Client
↓
Amazon API Gateway
↓
FastAPI (AWS Lambda via Mangum)
↓
FAISS Vector Store
↓
LLM (Mock / Local)

Flow:

Internal documents are ingested and indexed into FAISS

User requests hit API Gateway and are forwarded to Lambda

FastAPI handles routing and retrieval logic

Relevant document chunks are retrieved

Context is passed to an LLM layer to generate answers

---

## 📂 Project Structure

```text
internal-docs-rag-chatbot/
├── src/
│   ├── app.py              # FastAPI entry point (Mangum Lambda handler)
│   ├── ingest.py           # Document ingestion & indexing
│   ├── chat_local.py       # Local LLM logic
│   ├── chat_mock.py        # Mock LLM (no API cost)
│   ├── config.py           # Environment configuration
│   └── aws/                # AWS-specific helpers
├── data/                   # Internal documents
├── Dockerfile              # Lambda-compatible Docker image
├── requirements.txt
├── requirements-lambda.txt
├── test_fastapi.py         # API testing
└── README.md
```

## ⚙️ Tech Stack

- Language: Python 3.10+

- API Framework: FastAPI

- RAG Framework: LangChain

- Vector Search: FAISS

- API Layer: Amazon API Gateway (REST API)

- Deployment: AWS Lambda, Amazon ECR

- Container Registry: Amazon ECR

- Containerization: Docker

## 🐳 Run Locally (Lambda Runtime)

### Build image

```bash
docker build -t rag-chatbot-lambda .
Run container
docker run --rm -p 9000:8080 rag-chatbot-lambda
```
### Test Lambda locally
```bash
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -H "Content-Type: application/json" \
  -d '{"httpMethod":"GET","path":"/health"}'
``` 

## ☁️ AWS Deployment
1. Build Docker image locally

2. Push image to Amazon ECR

3. Create AWS Lambda function (Image type)

4. Configure Amazon API Gateway to route HTTP requests to Lambda

5. Deploy API Gateway stage (/prod)

6. Test endpoints via API Gateway

## Available Endpoints
```
GET  /health
POST /chat 
```
✅ Successfully deployed and tested on AWS Lambda behind API Gateway
✅ Deployment handled manually via Docker + AWS CLI

## 🧪 Development Mode
`chat_mock.py` allows running the full RAG flow without calling external LLM APIs

Suitable for:

- Local testing

- Demonstration

- Cost-free development

## 🎯 What This Project Demonstrates
- Practical RAG system implementation using LangChain

- Real-world Docker → ECR → Lambda → API Gateway workflow

- Understanding of serverless constraints

- REST API design and request routing via Amazon API Gateway

- Ability to build cost-aware, production-style backend systems
## 👤 Author
Hoàng Tuyến
Project built for hands-on learning and job applications.