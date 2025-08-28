from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status_id: int = 1
    flag_id: int = 1

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    flag_id: Optional[int] = None

class Task(TaskBase):
    id: int
    
    class Config:
        from_attributes = True
