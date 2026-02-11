# query_pipeline.py

import os
from dotenv import load_dotenv


load_dotenv()
from pinecone import Pinecone
from confidence import compute_retrieval_confidence

# ✅ DEFINE pc HERE (this was missing)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def query_role_context(query_embedding, top_k=3):
    index = pc.Index(os.getenv("PINECONE_INDEX"))

    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    matches = result.matches or []

    confidence = compute_retrieval_confidence(matches)
    contexts = [m.metadata for m in matches]

    return contexts, float(confidence)
