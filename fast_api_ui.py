
import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Budget 2024-2025 RAG Assistant",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# FASTAPI CONFIGURATION
# ============================================================

# LOCAL DEVELOPMENT
API_URL = "http://127.0.0.1:8000/ask"

# ------------------------------------------------------------
# FOR AZURE DEPLOYMENT:
# Replace the above URL with your Azure FastAPI URL.
#
# Example:
# API_URL = "https://your-fastapi-app.azurewebsites.net/ask"
# ------------------------------------------------------------


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Page background ---------- */

    .stApp {
        background: linear-gradient(
            180deg,
            #0f2027 0%,
            #203a43 50%,
            #2c5364 100%
        );
        color: #f5f5f5;
    }


    /* ---------- Main content width / padding ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }


    /* ---------- Title ---------- */

    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-align: center;
        letter-spacing: 0.5px;
    }


    /* ---------- Subheaders ---------- */

    h2,
    h3 {
        color: #f6c945 !important;
        font-weight: 700 !important;
    }


    /* ---------- Body text ---------- */

    p,
    li,
    span,
    label {
        color: #e8e8e8 !important;
    }


    /* ---------- Divider ---------- */

    hr {
        border: 1px solid rgba(255, 255, 255, 0.15);
    }


    /* ---------- Expander ---------- */

    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        color: #ffffff !important;
        font-weight: 600;
    }

    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.04);
        border-radius: 0 0 10px 10px;
        padding: 10px 15px;
    }


    /* ---------- Text input box ---------- */

    div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }

    input {
        color: #000000 !important;
        font-weight: 500;
    }

    input::placeholder {
        color: #555555 !important;
        opacity: 1;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        background: linear-gradient(
            90deg,
            #f6c945,
            #f29c1f
        );

        color: #000000 !important;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }


    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 6px 14px rgba(246, 201, 69, 0.35);

        color: #000000 !important;
    }


    /* ---------- Ensure button text stays black ---------- */

    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #000000 !important;
        font-weight: 700;
    }


    /* ---------- Answer card ---------- */

    .answer-card {
        background-color: rgba(255, 255, 255, 0.08);

        border-left: 5px solid #f6c945;

        border-radius: 12px;

        padding: 1.2rem 1.5rem;

        margin-top: 1rem;

        line-height: 1.6;

        font-size: 1.02rem;

        color: #ffffff;
    }


    /* ---------- Caption / footer ---------- */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        text-align: center;
        color: #cfcfcf !important;
    }


    /* ---------- Warning / error boxes ---------- */

    .stAlert p {
        color: #1a1a1a !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.title("📚 Budget 2024-2025 RAG Assistant")

st.write(
    "Ask questions about the Government of India's "
    "**Budget 2024-2025** speech and get answers grounded "
    "directly in the source document."
)

st.divider()


# ============================================================
# DOCUMENT INFORMATION
# ============================================================

with st.expander("📄 About the Document", expanded=False):

    st.markdown(
        """
        **Document:** Union Budget 2024-2025 Speech

        **Source:** Government of India

        **Document Type:** PDF

        **RAG System:** Pinecone + SentenceTransformer + Groq

        You can ask questions about topics such as agriculture,
        employment, infrastructure, education, taxation and
        other areas discussed in the Budget speech.
        """
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.subheader("💡 Example Questions")

example_questions = [
    "What are the main priorities of the Budget 2024-2025?",
    "What is the government's focus on agriculture?",
    "What does the Budget say about employment and skilling?",
    "What are the government's plans for infrastructure?",
]

cols = st.columns(2)

for i, question in enumerate(example_questions):

    with cols[i % 2]:

        if st.button(
            question,
            use_container_width=True,
            key=f"example_{i}",
        ):
            st.session_state["question"] = question


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader("🔎 Your Question")

question = st.text_input(
    label="Ask a question about the Budget speech",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What are the main priorities of the Budget?",
    label_visibility="collapsed",
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button(
    "🚀 Ask Question",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner(
                "🔍 Searching the Budget document and generating answer..."
            ):

                # ------------------------------------------------
                # SEND QUESTION TO FASTAPI
                # ------------------------------------------------

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120,
                )

                # ------------------------------------------------
                # CHECK FASTAPI RESPONSE
                # ------------------------------------------------

                response.raise_for_status()

                # ------------------------------------------------
                # CONVERT RESPONSE TO JSON
                # ------------------------------------------------

                data = response.json()

                # ------------------------------------------------
                # GET ANSWER
                # ------------------------------------------------

                answer = data.get("answer")

                if not answer:
                    st.error(
                        "❌ FastAPI returned a response, "
                        "but no answer was found."
                    )

                else:

                    # ------------------------------------------------
                    # DISPLAY ANSWER
                    # ------------------------------------------------

                    st.subheader("💬 Answer")

                    st.markdown(
                        f"""
                        <div class="answer-card">
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


        # ========================================================
        # ERROR HANDLING
        # ========================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to the FastAPI server."
            )

            st.info(
                "Please make sure your FastAPI server is running "
                "and the API_URL is correct."
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request took too long."
            )

            st.info(
                "Please try again. The RAG pipeline may be "
                "taking longer than expected."
            )


        except requests.exceptions.HTTPError as e:

            st.error(
                "❌ FastAPI returned an HTTP error "
                "while processing your question."
            )

            st.exception(e)


        except requests.exceptions.JSONDecodeError:

            st.error(
                "❌ FastAPI did not return a valid JSON response."
            )

            st.code(response.text)


        except KeyError:

            st.error(
                "❌ The FastAPI response does not contain "
                "the expected 'answer' field."
            )

            st.write("FastAPI response:")

            st.json(data)


        except Exception as e:

            st.error(
                "❌ Something went wrong while generating the answer."
            )

            st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Powered by SentenceTransformer • Pinecone • Groq • FastAPI • Streamlit"
)

