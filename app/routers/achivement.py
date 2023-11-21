from app.schemas.achievement import AchievementOut
from app.services.user import UserService
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.achievement import AchievementService

router = APIRouter(tags=["Achievement"], prefix="/achievement")



@router.get("/get_achievement_by_id/{achievement_id}", status_code=status.HTTP_200_OK)
async def get_achievement_by_id(
    achievement_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(UserService.get_current_user),

) -> AchievementOut:
    return await AchievementService.get_achievement_by_id(achievement_id, session)

@router.get("/get_achievement_by_user_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_achievement_by_user_id(
    user_id: int,
    # current_user=Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session)
    ) -> list[AchievementOut]:

    return await AchievementService.get_achievements_by_user_id(user_id,session)


@router.get("/get_all_achievement", status_code=status.HTTP_200_OK)
async def get_all_achievement(session: AsyncSession = Depends(get_session),    
                        # current_user=Depends(UserService.get_current_user),
                        ) -> list[AchievementOut]:
    return await AchievementService.get_all_achievements(session)

