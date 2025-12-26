# src/chat.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import pipeline

from config import VECTORSTORE_DIR, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME


def chat():
    print("🤖 Initializing Internal Docs RAG Chatbot...")

    # 1. Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )

    # 2. Load FAISS
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # 3. Retriever (chính xác hơn số lượng)
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    # 4. Local LLM (ổn định cho QA)
    hf_pipeline = pipeline(
        task="text-generation",
        model=LLM_MODEL_NAME,
        max_new_tokens=128,
        temperature=0.1,
        do_sample=False,
        repetition_penalty=1.1,
        truncation=True
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # 5. RAG chain – ép hành vi qua instruction ngắn
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "verbose": False
        },
        return_source_documents=True
    )

    print("✅ Chatbot ready! Type 'exit' to quit.")

    # 6. Chat loop
    while True:
        query = input("\n❓ Question: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        result = qa_chain.invoke({"query": query})
        answer = result.get("result", "").strip()

        # ✅ FIX TRẢ LỜI RỖNG / LINH TINH
        if not answer or len(answer) < 5:
            answer = "Không tìm thấy thông tin này trong tài liệu nội bộ."

        print("\n🤖 Answer:")
        print(answer)

        print("\n📚 Sources:")
        for doc in result["source_documents"]:
            print("-", doc.metadata.get("source", "unknown"))


if __name__ == "__main__":
    chat()
