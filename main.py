from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "1e90d58f-f936-8054-9f28-ffe10894e970"
NOTION_VERSION = "2022-06-28"

class TaskRequest(BaseModel):
    task_name: str
    description: str = "No description provided."
    task_type: str = "honey-do"
    status: str = "Assigned"

@app.post("/createTask")
def create_task(request: TaskRequest):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    status_map = {
        "Not Assigned": "89f166bf-11e7-4f12-8e63-7843d80d30c2",
        "Tardy :(": "rBK`",
        "Assigned": "d8e6a0b5-e57f-4609-bebf-8b92ad373d39",
        "Completed <3": "b950f3ad-38c9-4aeb-ae7d-a699a2106bfa"
    }

    payload = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": {
                "title": [{"text": {"content": request.task_name}}]
            },
            "Description": {
                "rich_text": [{"text": {"content": request.description}}]
            },
            "Type": {
                "select": {"name": request.task_type}
            },
            "Status": {
                "status": { "id": status_map.get(request.status, status_map["Assigned"]) }
            }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"message": "Task created successfully!"}