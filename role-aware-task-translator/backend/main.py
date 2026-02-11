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
    
class TaskResponse(BaseModel):
    role: str
    confidence: float
    confidence_level: str
    detailed_tasks: str    
    

@app.post("/translate-task",response_model=TaskResponse)
def translate_task(req: TaskRequest):
    issue_key = req.issue_key.strip().upper()

    # ---- Step 1: Fetch Jira issue ----
    task_title, task_description = get_jira_issue(issue_key)

    # ---- Step 2: Build query text ----
    query_text = f"{req.role}: {task_title}"
    if task_description:
        query_text += f". {task_description}"

    # ---- Step 3: Embedding ----
    query_embedding = generate_embedding(query_text)

    # ---- Step 4: Retrieval + confidence ----
    contexts, confidence = query_role_context(query_embedding)
    
    confidence=float(confidence or 0.0)

    # ---- Step 5: Prepare context for LLM ----
    context_text = "\n\n".join(
        f"Role: {c.get('role', '')}\n"
        f"Description: {c.get('role_description', '')}\n"
        f"Responsibilities: {c.get('responsibilities', '')}\n"
        f"Examples: {c.get('example_outputs', 'N/A')}"
        for c in contexts
    )

    # ---- Step 6: Generate tasks ----
    tasks = generate_tasks_with_context(
        task_title=task_title,
        task_description=task_description,
        role=req.role,
        context=context_text
    )

    # ---- Step 7: Confidence category ----
    if confidence >= 75:
        confidence_level = "HIGH"
    elif confidence >= 50:
        confidence_level = "MEDIUM"
    else:
        confidence_level = "LOW"
        
        
        
    print("DEBUG RESPONSE →", {
        "confidence": confidence,
        "confidence_level": confidence_level
    })
    # ---- Step 8: Response ----
    return TaskResponse(
        role=req.role,
        confidence=confidence,
        confidence_level=confidence_level,
        detailed_tasks=tasks
    )

 #(venv) PS D:\BE_project_final\role-aware-task-translator\backend> uvicorn main:app
