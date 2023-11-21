from app.models.achievements import Achievement
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao


class AchievementDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, task_data) -> Achievement:
        _task = Achievement(**task_data)
        self.session.add(_task)
        await self.session.commit()
        await self.session.refresh(_task)
        return _task

    async def get_by_id(self, achievement_id: int) -> Achievement | None:
        statement = select(Achievement).where(Achievement.achievement_id == achievement_id)
        return await self.session.scalar(statement=statement)


    async def get_all(self) -> list[Achievement]:
        statement = select(Achievement).order_by(Achievement.achievement_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    
    async def get_achievement_by_user_id(self, user_id: int)-> list[Achievement]:
        statement = select(Achievement).where(Achievement.user_id == user_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Achievement))
        await self.session.commit()

    async def delete_by_id(self, achievement_id: int) -> Achievement | None:
        _achievement = await self.get_by_id(achievement_id=achievement_id)
        statement = delete(Achievement).where(Achievement.achievement_id == achievement_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _achievement
    
