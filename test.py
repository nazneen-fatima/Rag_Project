from Rag_pipeline1 import rag_pipeline


# ============================================================
# TEST QUESTIONS
# ============================================================

questions = [

    "Who is presenting the Budget 2024-2025?",

    "What are the main priorities of the Budget 2024-2025?",

    "What is the government's focus on agriculture?",

    "What does the Budget say about employment and skilling?",

    "What are the government's plans for infrastructure?",

]


# ============================================================
# RUN TESTS
# ============================================================

for i, question in enumerate(questions, start=1):

    print()
    print("===================================")
    print(f"QUESTION {i}")
    print("===================================")

    print("Question:", question)

    answer = rag_pipeline(question)

    print()
    print("Answer:")
    print(answer)

