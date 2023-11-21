from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class TasksBase(BaseModel):
    task_name: str 
    description : str
    start_date: date
    due_date: date
    points: Optional[int] = None
    status: Optional[bool] = None
    completed_date: Optional[datetime] = None
    user_id: int
    approved: Optional[bool] = None
    priority : int

    model_config = ConfigDict(from_attributes=True)

class TasksIn(TasksBase):
    pass

class TasksOut(TasksBase):
    task_id: int
    created_at: datetime

    
class TasksUpdate(BaseModel):
    task_id: int
    status: bool
    
class TasksCount(BaseModel):
    count: int
    


