# 📚 Internal Docs RAG Chatbot

A serverless **Retrieval-Augmented Generation (RAG)** chatbot deployed on **AWS Lambda using Docker container images**, designed to answer questions from internal documents efficiently and cost-effectively.

Built with **FastAPI + FAISS**, focusing on clean architecture, serverless deployment, and real-world backend practices.

---

## 🚀 Key Features

- Serverless deployment using **AWS Lambda (Container Image)**
- Dockerized **FastAPI** application (Lambda-compatible)
- Full RAG pipeline: document ingestion → chunking → embeddings → vector search
- **Mock LLM mode** for local testing and cost-free development
- Simple, maintainable backend structure (no unnecessary complexity)

---

## 🧠 Architecture Overview

Client
↓
FastAPI (AWS Lambda)
↓
FAISS Vector Store
↓
LLM (Mock / Local)

- Documents are ingested and indexed into **FAISS**
- User queries retrieve relevant chunks
- Context is passed to an **LLM layer** to generate answers

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

- Vector Search: FAISS

- Deployment: AWS Lambda, Amazon ECR

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
Build Docker image locally

Push image to Amazon ECR

Create AWS Lambda function (Image type)

Test via Lambda Console or Function URL

✅ Successfully deployed and tested on AWS Lambda

Deployment is done manually via Docker + AWS CLI

### 🧪 Development Mode
`chat_mock.py` allows running the full RAG flow without calling external LLM APIs

Suitable for:

Local testing

Demonstration

Cost-free development

## 🎯 What This Project Demonstrates
Practical RAG system implementation

Real-world Docker → ECR → Lambda workflow

Understanding of serverless constraints

Ability to design systems with cost-awareness and simplicity

## 👤 Author
Hoàng Tuyến
Project built for hands-on learning and job applications.