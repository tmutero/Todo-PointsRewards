from app.models.achievements import Achievement
from app.models.tasks import Tasks
from sqlalchemy import delete, select,func
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao


class TaskDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, task_data) -> Tasks:
        _task = Tasks(**task_data)
        self.session.add(_task)
        await self.session.commit()
        await self.session.refresh(_task)
        return _task
    
    async def count_tasks(self, user_id:int) -> Tasks:
        count_query = select(func.count().label("count")).select_from(Tasks).where(Tasks.user_id == user_id)
        result = await self.session.execute(count_query)
        count = result.scalar()
        return count
    
    
    async def count_achievement(self,user_id:int) -> Achievement:
        count_query = select(func.count().label("count")).select_from(Achievement).where(Achievement.user_id == user_id)
        result = await self.session.execute(count_query)
        count = result.scalar()
        return count
    
    async def count_rewards(self) -> Achievement:
        count_query = select(func.count().label("points_reward")).select_from(Achievement).where(Tasks.status == False)
        result = await self.session.execute(count_query)
        count = result.scalar()
        return count
    
    
    async def count_pending_tasks(self,user_id:int) -> Tasks:
        count_query = select(func.count().label("count")).select_from(Tasks).where(Tasks.status == False and Tasks.user_id == user_id)
        result = await self.session.execute(count_query)
        count = result.scalar()
        return count
   
    async def get_by_id(self, task_id: int) -> Tasks | None:
        statement = select(Tasks).where(Tasks.task_id == task_id)
        return await self.session.scalar(statement=statement)


    async def get_all(self) -> list[Tasks]:
        statement = select(Tasks).order_by(Tasks.task_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    
    async def get_tasks_by_user_id(self, user_id: int)-> list[Tasks]:
        statement = select(Tasks).where(Tasks.user_id == user_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Tasks))
        await self.session.commit()

    async def delete_by_id(self, task_id: int) -> Tasks | None:
        _role = await self.get_by_id(task_id=task_id)
        statement = delete(Tasks).where(Tasks.task_id == task_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _role
    
    async def get_by_name(self, name) -> Tasks | None:
        statement = select(Tasks).where(Tasks.task_name == name)
        return await self.session.scalar(statement=statement)
