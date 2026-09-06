
from fastapi import FastAPI
from pydantic import BaseModel

from Rag_pipeline1 import rag_pipeline


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Budget 2024-2025 RAG API",
    description="API for asking questions about the Budget 2024-2025 speech",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Budget 2024-2025 RAG API is running"
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = rag_pipeline(request.question)

    return {
        "question": request.question,
        "answer": answer
    }

