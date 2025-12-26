import os

# Đường dẫn tuyệt đối cho an toàn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# HuggingFace embedding model
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"

# LLM model (nhẹ, chạy CPU)
LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"