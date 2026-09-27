from langchain_core.output_parsers import StrOutputParser

from db_service import search_books

from rag_service import retrieve_documents

from prompt import get_library_prompt

from llm_provider import get_llm


# =========================================================
# LLM
# =========================================================

llm = get_llm()


# =========================================================
# PROMPT
# =========================================================

prompt = get_library_prompt()


# =========================================================
# FORMAT BOOK DATA
# =========================================================

def format_books(books):

    if not books:

        return "No matching books found."


    result = []


    for book in books:

        result.append(

            f"""
Book Code: {book['book_code']}

Title: {book['title']}

Author: {book['author']}

Genre: {book['genre']}

Price: ₹{book['price']}

Available Copies: {book['available_copies']}

Format: {book['format']}
"""
        )


    return "\n".join(result)


# =========================================================
# BOOK DATABASE SEARCH
# =========================================================

def get_book_data(question):

    question_lower = question.lower()


    keywords = [

        "book",

        "books",

        "title",

        "author",

        "fiction",

        "history",

        "computer science",

        "machine learning",

        "price",

        "cost",

        "copies",

        "available",

        "format",

        "paperback",

        "hardcover",

        "ebook"
    ]


    found_keywords = []


    for keyword in keywords:

        if keyword in question_lower:

            found_keywords.append(
                keyword
            )


    # No book-related keyword
    if not found_keywords:

        return "No book catalog lookup required."


    books = []


    for keyword in found_keywords:

        results = search_books(
            keyword
        )

        books.extend(results)


    # =====================================================
    # REMOVE DUPLICATE BOOKS
    # =====================================================

    unique_books = {}


    for book in books:

        unique_books[
            book["book_code"]
        ] = book


    books = list(
        unique_books.values()
    )


    return format_books(
        books
    )


# =========================================================
# RAG CONTEXT
# =========================================================

def get_rag_context(question):

    documents = retrieve_documents(
        question
    )


    if not documents:

        return "No relevant information found."


    context = []


    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown"
        )


        context.append(

            f"""
Source: {source}

{document.page_content}
"""
        )


    return "\n".join(context)


# =========================================================
# MAIN CHAT FUNCTION
# =========================================================

def ask_question(question):

    # -----------------------------------------------------
    # STEP 1: DATABASE CALL
    # -----------------------------------------------------

    book_data = get_book_data(question)


    # -----------------------------------------------------
    # STEP 2: RAG CALL
    # -----------------------------------------------------

    rag_context = get_rag_context(question)


    # -----------------------------------------------------
    # STEP 3: CREATE LANGCHAIN CHAIN
    # -----------------------------------------------------

    chain = ( prompt | llm |  StrOutputParser() )


    # -----------------------------------------------------
    # STEP 4: SEND DATA TO CHAIN and Execute that chain
    # -----------------------------------------------------

    answer = chain.invoke(

        {
            "book_data": book_data,
            "rag_context": rag_context,
            "question": question
        }
    )


    return answer
