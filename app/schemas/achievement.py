from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class AchievementBase(BaseModel):
    
    achievement_date: datetime
    user_id : int
    delayed: bool
    achievement_details: str
    points_reward : int
    model_config = ConfigDict(from_attributes=True)


class AchievementIn(AchievementBase):
    pass

class AchievementOut(AchievementBase):
    achievement_id: int
    
    


