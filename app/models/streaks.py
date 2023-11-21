from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Streaks(Base):
    __tablename__ = "streaks"

    streak_id: Mapped[intpk]
    created_date =  mapped_column(DateTime)
    end_date = mapped_column(DateTime)
    user_id :  Mapped[int]
   
    
    

