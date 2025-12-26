# src/ingest.py

import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


from config import DATA_DIR, VECTORSTORE_DIR, EMBEDDING_MODEL_NAME


def ingest():
    print("📥 Loading documents...")
    documents = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(path, encoding="utf-8")
            documents.extend(loader.load())

    print(f"✅ Loaded {len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=120,        # nhỏ để giữ 1 ý / chunk
        chunk_overlap=20,
        separators=[
            "\n\n",            # ưu tiên ngắt theo đoạn
            "\n",
            ". ",
            " "
        ]
    )
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)

    print("🎉 Vectorstore created successfully!")


if __name__ == "__main__":
    ingest()
