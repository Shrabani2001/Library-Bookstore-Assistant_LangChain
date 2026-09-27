# Library & Bookstore Assistant (LLaMA + Chroma)

A different app from the student-assistant example, built in the **same flow**:

```
Streamlit UI (app.py)
        │
        ▼
chatbot_chain.py  ──►  db_service.py   (SQLite book catalog lookup)
        │        ──►  rag_service.py  (Chroma vector search over policy docs)
        │
        ▼
prompt.py + llm_provider.py (local LLaMA via Ollama)
```

| Piece        | Stack                                |
|--------------|----------------------------------------|
| Chat model   | Local LLaMA model via **Ollama**       |
| Embeddings   | Ollama embedding model (`nomic-embed-text`) |
| Vector store | **Chroma** (persisted to local disk)   |
| Structured data | SQLite book catalog (title, author, genre, price, copies, format) |
| RAG source   | `documents/library_policy.txt` (membership, borrowing, late fees, hours) |

## 1. Install Ollama and pull models

```bash
ollama pull llama3
ollama pull nomic-embed-text
ollama serve
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment

```bash
cp ..env .env
```

## 4. Ingest the knowledge base

A sample policy file is already in `documents/library_policy.txt`. Add more
`.txt` files there, then run:

```bash
python rag_service.py
```

This embeds and stores the chunks in the local `chroma_db/` folder.

## 5. Run the app

```bash
streamlit run app.py
```

## Files

- `app.py` — Streamlit chat UI, sidebar catalog and example questions
- `chatbot_chain.py` — orchestrates catalog lookup + RAG retrieval + LLM chain
- `db_service.py` — SQLite book catalog (seeded with 4 sample books)
- `rag_service.py` — Chroma ingestion and retrieval
- `prompt.py` — prompt template combining catalog + RAG context
- `llm_provider.py` — local LLaMA via Ollama
- `config.py` — Ollama/Chroma settings from `.env`
