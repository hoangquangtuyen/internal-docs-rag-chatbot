📚 Internal Docs RAG Chatbot

Một project RAG (Retrieval-Augmented Generation) Chatbot dùng dữ liệu nội bộ (PDF, DOCX, Markdown, TXT, …), có thể chạy local, Docker, và deploy trên AWS Lambda. Project được thiết kế theo hướng modular, dễ mở rộng, và phù hợp để đưa vào CV / Portfolio.

🚀 Tính năng chính

🔍 RAG pipeline: ingest tài liệu → embedding → lưu vectorstore → truy vấn + sinh câu trả lời

🤖 2 chế độ chat:

chat_local.py: dùng LLM thật (Gemini / HuggingFace / …)

chat_mock.py: mock LLM (không cần API key, phù hợp demo & deploy Lambda)

📦 Vectorstore FAISS (offline, nhẹ, nhanh)

🐳 Docker-ready (chạy local & Lambda container)

☁️ AWS Lambda compatible (image-based deployment)

🔐 Quản lý cấu hình & API key qua .env

🏗️ Kiến trúc tổng quan
User Query
   ↓
Retriever (FAISS)
   ↓
Relevant Chunks
   ↓
LLM (Local / Mock / API)
   ↓
Final Answer

Mock mode giúp tách biệt business logic và LLM provider, rất phù hợp trong môi trường không có chi phí API.

📂 Cấu trúc thư mục
internal-docs-rag-chatbot/
│
├── data/                   # Dữ liệu đầu vào (pdf, docx, md, txt…)
├── src/
│   ├── app.py               # Entry point (FastAPI / Lambda handler)
│   ├── ingest.py            # Ingest & build vectorstore
│   ├── chat_local.py        # Chat với LLM thật
│   ├── chat_mock.py         # Chat mock (không cần API key)
│   ├── config.py            # Load config & env
│   └── aws/
│       ├── dist/            # Build artifacts cho Lambda
│       └── install/         # Dependencies Lambda
│
├── requirements.txt         # Dependencies local
├── requirements-lambda.txt  # Dependencies cho Lambda
├── Dockerfile               # Docker & Lambda image
├── test_fastapi.py          # Test API
├── response.json            # Sample response
├── .env.example             # Mẫu biến môi trường
└── README.md
⚙️ Cài đặt & chạy local
1️⃣ Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
2️⃣ Cài dependencies
pip install -r requirements.txt
3️⃣ Cấu hình biến môi trường

Tạo file .env:

LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_api_key_here

⚠️ Có thể không cần API key nếu dùng chat_mock.py

📥 Ingest dữ liệu
python src/ingest.py

Script sẽ:

Load tài liệu trong data/

Split text

Tạo embedding

Lưu FAISS vectorstore

💬 Chạy chatbot
Mock mode (khuyến nghị để demo / Lambda)
python src/chat_mock.py
Local LLM / API mode
python src/chat_local.py
🐳 Chạy bằng Docker
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot

Test:

http://localhost:8000/docs
☁️ Deploy AWS Lambda (Container Image)

Base image: public.ecr.aws/lambda/python

Entry point: src/app.py

Không phụ thuộc API key khi dùng mock mode

👉 Phù hợp cho free-tier / demo / interview project

👤 Tác giả
Hoàng Tuyến