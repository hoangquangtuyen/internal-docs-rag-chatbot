import os
from pathlib import Path

# =========================
# 📂 PROJECT PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# =========================
# 🔍 EMBEDDING MODEL
# =========================
EMBEDDING_MODEL_NAME = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# =========================
# ✂️ TEXT SPLITTING (BẮT BUỘC cho ingest.py)
# =========================
CHUNK_SIZE = 800          # tốt cho PDF / DOC tiếng Việt
CHUNK_OVERLAP = 150      # giúp không mất ngữ cảnh

# =========================
# ⚙️ RAG PARAMETERS (dùng cho chat.py)
# =========================
TOP_K = 5
TEMPERATURE = 0.1
MAX_OUTPUT_TOKENS = 512

# =========================
# 🔎 SEARCH SETTINGS
# =========================
SEARCH_TYPE = "similarity"   # "similarity" | "mmr"
MMR_DIVERSITY = 0.3
