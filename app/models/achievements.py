from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Achievement(Base):
    __tablename__ = "achievement"

    achievement_id: Mapped[intpk]
    achievement_date = mapped_column(DateTime)
    user_id :  Mapped[int]
    delayed: Mapped[bool]
    achievement_details: Mapped[str100]
    points_reward : Mapped[int]
   
    
    

