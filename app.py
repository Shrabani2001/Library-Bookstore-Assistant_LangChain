import streamlit as st

from db_service import (
    initialize_database,
    get_all_books
)

from chatbot_chain import ask_question
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(

    page_title="Library & Bookstore Assistant",

    page_icon="📚",

    layout="wide"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

initialize_database()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {

        font-size: 38px;

        font-weight: 700;

        color: #92400E;

        text-align: center;

        margin-bottom: 5px;
    }


    .subtitle {

        text-align: center;

        color: #6B7280;

        margin-bottom: 30px;
    }


    .book-card {

        background-color: #FFFBEB;

        padding: 15px;

        border-radius: 10px;

        margin-bottom: 10px;

        border: 1px solid #FDE68A;
    }


    </style>
    """,

    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 Library Assistant")


    st.write(
        "Local LLaMA powered book & policy chatbot"
    )


    st.divider()


    # -----------------------------------------------------
    # BOOK LIST
    # -----------------------------------------------------

    st.subheader("📖 Catalog")


    books = get_all_books()


    for book in books:

        st.markdown(

            f"""
            <div class="book-card">

            <b>{book['book_code']}</b> — {book['title']}

            <br>

            by {book['author']}

            <br><br>

            💰 ₹{book['price']} · {book['format']}

            <br>

            📦 {book['available_copies']} copies available

            </div>
            """,

            unsafe_allow_html=True
        )


    st.divider()


    # -----------------------------------------------------
    # EXAMPLE QUESTIONS
    # -----------------------------------------------------

    st.subheader(
        "💡 Example Questions"
    )


    examples = [

        "What books do you have on machine learning?",

        "What is the price of Whispers of the Deccan?",

        "How many copies of Data Structures Simplified are available?",

        "What is the late fee policy?",

        "How many books can I borrow at once?",

        "What are the membership plans?"
    ]


    for example in examples:

        if st.button(

            example,

            use_container_width=True
        ):

            st.session_state[
                "selected_question"
            ] = example


    st.divider()


    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.button(

        "🗑️ Clear Chat",

        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(

    """
    <div class="main-title">

        📚 Library & Bookstore Assistant

    </div>

    <div class="subtitle">

        Ask about books, prices, availability,
        membership and borrowing policies.

    </div>
    """,

    unsafe_allow_html=True
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# USER INPUT
# =========================================================

question = st.chat_input(

    "Ask your question..."
)


# =========================================================
# SIDEBAR QUESTION
# =========================================================

if "selected_question" in st.session_state:

    question = st.session_state.pop(
        "selected_question"
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # DISPLAY USER QUESTION
    # -----------------------------------------------------

    st.session_state.messages.append(

        {
            "role": "user",

            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # -----------------------------------------------------
    # GET AI RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                answer = ask_question(
                    question
                )


            except Exception as e:

                answer = (

                    "❌ Sorry, something went wrong.\n\n"

                    f"Error: {str(e)}"
                )


        st.markdown(answer)


    # -----------------------------------------------------
    # SAVE AI RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": answer
        }
    )
