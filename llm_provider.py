from langchain_ollama import ChatOllama

from config import (
    OLLAMA_CHAT_MODEL,
    OLLAMA_BASE_URL
)


# =========================================================
# CREATE LOCAL LLAMA LLM (via Ollama)
# =========================================================

def get_llm():

    llm = ChatOllama(

        model=OLLAMA_CHAT_MODEL,

        base_url=OLLAMA_BASE_URL,

        temperature=0
    )

    return llm
