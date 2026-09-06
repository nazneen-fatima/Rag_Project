
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in .env")


# ============================================================
# LOAD PDF
# ============================================================

loader = PyPDFLoader("data/budget_speech.pdf")

documents = loader.load()

print("Number of pages:", len(documents))


# ============================================================
# SPLIT DOCUMENT INTO CHUNKS
# ============================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Number of chunks:", len(chunks))


# ============================================================
# PREPARE TEXT AND METADATA
# ============================================================

texts = [chunk.page_content for chunk in chunks]

metadatas = [chunk.metadata for chunk in chunks]


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)


# ============================================================
# CONNECT TO PINECONE
# ============================================================

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index("sentence-transformer-index1")

print("Connected to Pinecone")


# ============================================================
# PREPARE VECTORS
# ============================================================

vectors = []

for i in range(len(embeddings)):
    vectors.append(
        {
            "id": str(i),
            "values": embeddings[i].tolist(),
            "metadata": {
                "text": texts[i],
                "page": metadatas[i].get("page", 0)
            }
        }
    )

print("Vectors prepared:", len(vectors))


# ============================================================
# UPLOAD VECTORS TO PINECONE
# ============================================================

index.upsert(vectors=vectors)

print("Vectors uploaded successfully")


# ============================================================
# CHECK PINECONE
# ============================================================

stats = index.describe_index_stats()

print("Pinecone index statistics:")

print(stats)


print()

print("===================================")
print("INGESTION COMPLETED SUCCESSFULLY")
print("===================================")


