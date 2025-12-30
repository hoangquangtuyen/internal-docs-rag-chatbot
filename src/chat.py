import sys
import os
import torch

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from config import (
    VECTORSTORE_DIR,
    EMBEDDING_MODEL_NAME,
    TOP_K,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    SEARCH_TYPE,
    MMR_DIVERSITY
)

# =========================
# 🎯 PROMPT TEMPLATE
# =========================
PROMPT_TEMPLATE = """Bạn là một trợ lý AI chuyên trả lời câu hỏi dựa trên tài liệu nội bộ.

NGUYÊN TẮC:
1. CHỈ trả lời dựa trên thông tin từ tài liệu bên dưới
2. Nếu không có thông tin, nói rõ: "Tôi không tìm thấy thông tin trong tài liệu"
3. Trả lời bằng tiếng Việt, ngắn gọn, súc tích

TÀI LIỆU THAM KHẢO:
{context}

CÂU HỎI: {input}

TRẢ LỜI:
"""

# =========================
# 🚀 INIT CHATBOT
# =========================
def initialize_chatbot():
    try:
        print("🔄 Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        print("🔄 Loading vectorstore...")
        if not VECTORSTORE_DIR.exists():
            raise FileNotFoundError(
                f"Vectorstore not found at {VECTORSTORE_DIR}. "
                "Please run ingest.py first."
            )

        vectorstore = FAISS.load_local(
            str(VECTORSTORE_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )

        # =========================
        # 🔍 RETRIEVER
        # =========================
        if SEARCH_TYPE == "mmr":
            retriever = vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": TOP_K,
                    "fetch_k": TOP_K * 2,
                    "lambda_mult": MMR_DIVERSITY
                }
            )
            print(f"✅ Using MMR retriever (diversity={MMR_DIVERSITY})")
        else:
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": TOP_K}
            )
            print(f"✅ Using similarity retriever (top_k={TOP_K})")

        # =========================
        # 🤖 LOCAL LLM (QWEN)
        # =========================
        print("🔄 Loading local LLM: Qwen2.5-3B-Instruct")

        model_id = "Qwen/Qwen2.5-3B-Instruct"

        tokenizer = AutoTokenizer.from_pretrained(model_id)

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        text_gen_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=MAX_OUTPUT_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True
        )

        llm = HuggingFacePipeline(pipeline=text_gen_pipeline)

        # =========================
        # 🔗 LCEL RAG CHAIN
        # =========================
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        rag_chain = (
            {
                "context": retriever,
                "input": RunnablePassthrough()
            }
            | prompt
            | llm
        )

        print("✅ Chatbot ready (Local LLM)")
        return rag_chain

    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        sys.exit(1)

# =========================
# 💬 CHAT LOOP
# =========================
def chat():
    print("\n" + "=" * 60)
    print("🤖 Internal Docs RAG Chatbot (LOCAL LLM)")
    print("=" * 60)

    rag_chain = initialize_chatbot()

    print("\n💡 Tips:")
    print("  • Type 'exit' or 'quit' to quit")
    print("  • Type 'clear' to clear screen")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("❓ Your question: ").strip()

            if not query:
                continue

            if query.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye!")
                break

            if query.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue

            print("\n🔍 Searching documents...")
            response = rag_chain.invoke(query)

            print("\n" + "─" * 60)
            print("🤖 Answer:")
            print("─" * 60)
            print(response)
            print("=" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

# =========================
# ▶️ MAIN
# =========================
if __name__ == "__main__":
    chat()
