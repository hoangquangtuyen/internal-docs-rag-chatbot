import os
from pathlib import Path
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import (
    BASE_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

# ==============================
# 📂 DATA DIRECTORY
# ==============================
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ==============================
# 📄 SUPPORTED FILE TYPES
# ==============================
SUPPORTED_EXTENSIONS = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
    ".md": UnstructuredMarkdownLoader,
}

# ==============================
# LOAD SINGLE DOCUMENT
# ==============================
def load_document(file_path: Path) -> List[Document]:
    try:
        ext = file_path.suffix.lower()

        if ext not in SUPPORTED_EXTENSIONS:
            print(f"⚠️ Skip unsupported: {file_path.name}")
            return []

        loader_class = SUPPORTED_EXTENSIONS[ext]

        if ext == ".txt":
            loader = loader_class(str(file_path), encoding="utf-8")
        else:
            loader = loader_class(str(file_path))

        docs = loader.load()

        for doc in docs:
            doc.metadata.update({
                "source": file_path.name,
                "file_type": ext,
                "file_path": str(file_path)
            })

        print(f"✅ Loaded: {file_path.name} ({len(docs)} pages)")
        return docs

    except Exception as e:
        print(f"❌ Error loading {file_path.name}: {e}")
        return []

# ==============================
# LOAD ALL DOCUMENTS
# ==============================
def load_all_documents() -> List[Document]:
    print(f"\n📂 Scanning: {DATA_DIR}")

    files = [f for f in DATA_DIR.rglob("*") if f.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not files:
        raise ValueError("❌ No supported documents found")

    print(f"📄 Found {len(files)} files")
    print("-" * 60)

    documents = []
    for file in files:
        documents.extend(load_document(file))

    return documents

# ==============================
# SPLIT DOCUMENTS
# ==============================
def split_documents(documents: List[Document]) -> List[Document]:
    print(f"\n✂️ Splitting documents...")
    print(f"Chunk size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")

    return chunks

# ==============================
# CREATE VECTORSTORE
# ==============================
def create_vectorstore(chunks: List[Document]):
    print(f"\n🔮 Embedding model: {EMBEDDING_MODEL_NAME}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cuda"},   # ⚡ GPU (Colab)
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 16
        }
    )

    print("🔄 Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"✅ Vectorstore saved at: {VECTORSTORE_DIR}")

# ==============================
# DISPLAY STATS
# ==============================
def display_stats(chunks: List[Document]):
    print("\n" + "=" * 60)
    print("📊 INGESTION STATS")
    print("=" * 60)

    sources = set()
    types = {}

    for c in chunks:
        sources.add(c.metadata.get("source"))
        t = c.metadata.get("file_type")
        types[t] = types.get(t, 0) + 1

    print(f"📄 Total chunks: {len(chunks)}")
    print(f"📁 Total files: {len(sources)}")

    print("\nChunks by type:")
    for k, v in types.items():
        print(f"  {k}: {v}")

    if chunks:
        sample = chunks[0]
        print("\n📝 Sample chunk:")
        print(sample.page_content[:200] + "...")

    print("=" * 60)

# ==============================
# MAIN PIPELINE
# ==============================
def ingest():
    print("\n" + "=" * 60)
    print("🚀 STARTING INGESTION")
    print("=" * 60)

    docs = load_all_documents()
    chunks = split_documents(docs)
    create_vectorstore(chunks)
    display_stats(chunks)

    print("\n✅ INGEST COMPLETED")
    print("👉 Next step: build chat.py")

# ==============================
if __name__ == "__main__":
    ingest()
