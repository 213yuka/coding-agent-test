from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    due_date: Optional[date]

    model_config = {"from_attributes": True}
