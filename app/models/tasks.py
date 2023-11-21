import datetime
from sqlalchemy import String, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100, str250


class Tasks(Base):
    __tablename__ = "tasks"

    task_id: Mapped[intpk]
    task_name: Mapped[str100]
    description: Mapped[str250]
    start_date =  mapped_column(Date)
    due_date =  mapped_column(Date)
    points :  Mapped[int]
    priority: Mapped[int]
    status: Mapped[bool | None]
    approved: Mapped[bool | None ]
    completed_date = mapped_column(DateTime, nullable=True)
    user_id : Mapped[int]
    created_at = mapped_column(DateTime,default=datetime.datetime.utcnow)
    
    

