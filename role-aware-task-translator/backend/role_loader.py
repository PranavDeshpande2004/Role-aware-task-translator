# import csv
# import pinecone
# import os
# from embedding_pipeline import generate_embedding

# def load_roles_to_pinecone(csv_path):
#     pinecone.init(
#         api_key=os.getenv("PINECONE_API_KEY"),
#         environment=os.getenv("PINECONE_ENV")
#     )

#     index = pinecone.Index(os.getenv("PINECONE_INDEX"))

#     with open(csv_path, newline='', encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             vector = generate_embedding(row["description"] + " " + row["responsibilities"])
#             index.upsert([
#                 (
#                     row["role"],
#                     vector,
#                     row
#                 )
#             ])


from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
import os
import csv
from embedding_pipeline import generate_embedding

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

BATCH_SIZE = 2   # very safe for free tier

def load_roles_to_pinecone():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "roles.csv")

    vectors = []

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = f"{row['role_description']} {row['responsibilities']} {row['example_outputs']}"
            vectors.append({
                "id": row["role"],
                "values": generate_embedding(text),
                "metadata": {
                    "role": row["role"],
                    "role_description": row["role_description"],
                    "responsibilities": row["responsibilities"],
                    "example_outputs": row["example_outputs"]
                }
            })

    #  BATCH UPSERT
    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i + BATCH_SIZE]
        index.upsert(batch)
        #print(f" Uploaded batch {i//BATCH_SIZE + 1}")

    print(" All roles uploaded successfully")

if __name__ == "__main__":
    load_roles_to_pinecone()
