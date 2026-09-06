# import os

# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# from pinecone import Pinecone
# from groq import Groq


# # ============================================================
# # LOAD ENVIRONMENT VARIABLES
# # ============================================================

# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not PINECONE_API_KEY:
#     raise ValueError("PINECONE_API_KEY is not set in .env")

# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY is not set in .env")


# # ============================================================
# # LOAD EMBEDDING MODEL
# # ============================================================

# model = SentenceTransformer("all-MiniLM-L6-v2")


# # ============================================================
# # CONNECT TO PINECONE
# # ============================================================

# pc = Pinecone(api_key=PINECONE_API_KEY)

# index = pc.Index("sentence-transformer-index1")


# # ============================================================
# # CONNECT TO GROQ
# # ============================================================

# client = Groq(api_key=GROQ_API_KEY)


# # ============================================================
# # RETRIEVE RELEVANT DOCUMENT CHUNKS
# # ============================================================

# def retrieve(query, top_k=5):

#     print()
#     print("STEP 1: Creating query embedding...")

#     query_vec = model.encode(
#         query,
#         convert_to_numpy=True,
#         normalize_embeddings=True
#     )

#     print("STEP 2: Query embedding created")
#     print("Embedding dimension:", len(query_vec))

#     print("STEP 3: Querying Pinecone...")

#     results = index.query(
#         vector=query_vec.tolist(),
#         top_k=top_k,
#         include_metadata=True
#     )

#     print("STEP 4: Pinecone query completed")
#     print("Number of results:", len(results["matches"]))

#     return results["matches"]





# # ============================================================
# # GENERATE ANSWER USING GROQ
# # ============================================================

# def generate_answer(context, question):

#     prompt = f"""
# You are a helpful assistant.

# Use ONLY the context below to answer the question.

# If the answer is not present in the context, say:

# "I could not find the answer in the provided document."

# Context:
# {context}

# Question:
# {question}

# Answer clearly and concisely.
# """

#     response = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0
#     )

#     return response.choices[0].message.content


# # ============================================================
# # RAG PIPELINE
# # ============================================================

# def rag_pipeline(question):

#     docs = retrieve(question, top_k=15)

#     context = "\n\n".join(
#         doc["metadata"]["text"]
#         for doc in docs
#         if doc.get("metadata")
#         and doc["metadata"].get("text")
#      )

#     answer = generate_answer(context, question)

#     return answer


# # # ============================================================
# # # TEST THE RAG PIPELINE
# # # ============================================================

# if __name__ == "__main__":

#      query = "What are the main priorities of the Budget 2024-2025?"

#      answer = rag_pipeline(query)

#      print()
#      print("FINAL ANSWER:")
#      print(answer)


import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# CONNECT TO PINECONE
# ============================================================

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index("sentence-transformer-index1")


# ============================================================
# CONNECT TO GROQ
# ============================================================

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# RETRIEVE RELEVANT DOCUMENT CHUNKS
# ============================================================

def retrieve(query, top_k=15):

    query_vec = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    results = index.query(
        vector=query_vec.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    return results["matches"]


# ============================================================
# GENERATE ANSWER USING GROQ
# ============================================================

def generate_answer(context, question):

    prompt = f"""
You are a helpful assistant.

Use ONLY the context below to answer the question.

If the answer is not present in the context, say:

"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ============================================================
# RAG PIPELINE
# ============================================================

def rag_pipeline(question):

    docs = retrieve(question, top_k=15)

    context = "\n\n".join(
        doc["metadata"]["text"]
        for doc in docs
        if doc.get("metadata")
        and doc["metadata"].get("text")
    )

    answer = generate_answer(context, question)

    return answer












