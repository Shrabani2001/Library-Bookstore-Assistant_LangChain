from pathlib import Path

from langchain_chroma import Chroma

from langchain_ollama import OllamaEmbeddings

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import Document

from config import (
    OLLAMA_EMBEDDING_MODEL,
    OLLAMA_BASE_URL,
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME
)


def load_documents():

    documents = []

    folder = Path("documents")

    for file in folder.glob("*.txt"):

        text = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            Document(
                page_content=text,

                metadata={
                    "source": file.name
                }
            )
        )

    return documents


def get_embeddings():

    return OllamaEmbeddings(

        model=OLLAMA_EMBEDDING_MODEL,

        base_url=OLLAMA_BASE_URL
    )


def get_vector_store():

    embeddings = get_embeddings()

    vector_store = Chroma(

        collection_name=CHROMA_COLLECTION_NAME,

        embedding_function=embeddings,

        persist_directory=CHROMA_PERSIST_DIRECTORY
    )

    return vector_store


def ingest_documents():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Documents: {len(documents)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    vector_store = get_vector_store()

    vector_store.add_documents(
        chunks
    )

    print(
        "Documents added to Chroma."
    )


def retrieve_documents(question):

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    documents = retriever.invoke(
        question
    )

    return documents


if __name__ == "__main__":

    ingest_documents()
