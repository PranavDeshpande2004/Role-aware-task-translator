# import pinecone
# import os

# def query_roles(embedding, top_k=3):
#     pinecone.init(
#         api_key=os.getenv("PINECONE_API_KEY"),
#         environment=os.getenv("PINECONE_ENV")
#     )
#     index = pinecone.Index(os.getenv("PINECONE_INDEX"))
#     result = index.query(vector=embedding, top_k=top_k, include_metadata=True)
#     return result["matches"]



from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ REQUIRED

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# def query_roles(embedding, top_k=5):
#     index = pc.Index(os.getenv("PINECONE_INDEX"))

#     result = index.query(
#         vector=embedding,
#         top_k=top_k,
#         include_metadata=True
#     )
#     return result.matches


def query_role_context(query_embedding, top_k=5, direct_threshold=0.85):
    index = pc.Index(os.getenv("PINECONE_INDEX"))

    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    matches = result["matches"]
    if not matches:
        return []

    #  Direct match logic
    if matches[0]["score"] >= direct_threshold:
        return [matches[0]["metadata"]]

    # 🔁 Fallback to Top-K
    return [m["metadata"] for m in matches]


