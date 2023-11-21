from app.schemas.achievement import AchievementIn, AchievementOut
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.daos import achievement


class AchievementService:
    
    @staticmethod
    async def create_achievement(task_data: AchievementIn, session: AsyncSession):
        new_achievement = await achievement.AchievementDao(session).create(task_data)
        logger.info(f"New achievement created successfully: {task_data}!!!")
        return  new_achievement

 
    @staticmethod
    async def get_all_achievements(session: AsyncSession) -> list[AchievementOut]:
        all_achievements = await achievement.AchievementDao(session).get_all()
        return [AchievementOut.model_validate(_achievement) for _achievement in all_achievements]

   
    @staticmethod
    async def get_achievement_by_id(achievement_id: int, session: AsyncSession) -> AchievementOut:
        _achievement = await achievement.AchievementDao(session).get_by_id(achievement_id)
        if not _achievement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task with the given id does not exist!!!",
            )
        return AchievementOut.model_validate(_achievement)
    

    @staticmethod
    async def get_achievements_by_user_id(user_id: int,session: AsyncSession) -> list[AchievementOut]:
        all_achievements = await achievement.AchievementDao(session).get_achievement_by_user_id(user_id)
        return [AchievementOut.model_validate(_achievement) for _achievement in all_achievements]

    
