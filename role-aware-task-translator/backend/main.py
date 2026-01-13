# from fastapi import FastAPI
# from pydantic import BaseModel
# from embedding_pipeline import generate_embedding
# from query_pipeline import query_role_context
# from llm_generator import generate_tasks_with_context
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Optional
# from dotenv import load_dotenv
# load_dotenv()  #

# app = FastAPI()

# # ✅ CORS FIX
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class TaskRequest(BaseModel):
#     task_title: str
#     task_description: Optional[str] = ""   # 👈 optional
#     role: str



# @app.post("/translate-task")
# def translate_task(req: TaskRequest):

#     # 🔹 1. Build query text (role + task)
#     query_text = f"{req.role}: {req.task_title}"
#     if req.task_description:
#         query_text += f". {req.task_description}"

#     # 🔹 2. Create embedding
#     query_embedding = generate_embedding(query_text)

#     # 🔹 3. Retrieve context (direct match OR top-K)
#     contexts = query_role_context(query_embedding)

#     # 🔹 4. Build context text
#     context_text = "\n\n".join([
#         f"Role: {c['role']}\n"
#         f"Description: {c['role_description']}\n"
#         f"Responsibilities: {c['responsibilities']}\n"
#         f"Examples: {c['example_outputs']}"
#         for c in contexts
#     ])

#     # 🔹 5. Generate ONE role-specific response
#     tasks = generate_tasks_with_context(
#         task_title=req.task_title,
#         task_description=req.task_description,
#         role=req.role,
#         context=context_text
#     )

#     return {
#         "role": req.role,
#         "detailed_tasks": tasks
#     }


from fastapi import FastAPI
from pydantic import BaseModel
from embedding_pipeline import generate_embedding
from query_pipeline import query_role_context
from llm_generator import generate_tasks_with_context
from jira_client import get_jira_issue
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv(override=True)



app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    issue_key: str
    role: str

@app.post("/translate-task")
def translate_task(req: TaskRequest):
    issue_key = req.issue_key.strip().upper()

    task_title, task_description = get_jira_issue(issue_key)

    query_text = f"{req.role}: {task_title}"
    if task_description:
        query_text += f". {task_description}"

    query_embedding = generate_embedding(query_text)
    contexts = query_role_context(query_embedding)

    context_text = "\n\n".join(
    f"Role: {c.get('role', '')}\n"
    f"Description: {c.get('role_description', '')}\n"
    f"Responsibilities: {c.get('responsibilities', '')}\n"
    f"Examples: {c.get('example_outputs', 'N/A')}"
    for c in contexts
)

    tasks = generate_tasks_with_context(
        task_title=task_title,
        task_description=task_description,
        role=req.role,
        context=context_text
    )

    return {
        "role": req.role,
        "detailed_tasks": tasks
    }


#(venv) PS D:\BE_project_final\role-aware-task-translator\backend> uvicorn main:app
