from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tasks_with_context(task_title, task_description, role, context):

    task_text = task_title
    if task_description:
        task_text += f". {task_description}"

    prompt = f"""
You are acting STRICTLY as a {role}.

Use ONLY the CONTEXT below.
Do NOT introduce tasks outside this role.

CONTEXT:
{context}

GENERIC TASK:
"{task_text}"

Generate a DETAILED, REAL-WORLD,
ROLE-SPECIFIC task breakdown.

Rules:
- One role only
- Bullet points
"""

    response = client.chat.completions.create(
        #model="gpt-4o-mini",
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
        #temperature=0.2
    )

    return response.choices[0].message.content
