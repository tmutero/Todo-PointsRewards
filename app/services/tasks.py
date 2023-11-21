from app.schemas.tasks import TasksCount, TasksIn, TasksOut, TasksUpdate
from app.services.achievement import AchievementService
from app.utils.points_utils import calculate_reward
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tasks import Tasks as TasksModel
from datetime import datetime

from app.daos import tasks
from app.daos import achievement


class TasksService:
    
    @staticmethod
    async def create_task(task_data: TasksIn, session: AsyncSession):
        task_exist = await TasksService.task_name_exists(session, task_data.task_name)

        if task_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task with the given name already exists!!!",
            )
        task_data.approved = False
        task_data.status = False
        new_task = await tasks.TaskDao(session).create(task_data.model_dump())
        logger.info(f"New tasks created successfully: {new_task}!!!")
        return JSONResponse(
            content={"message": "Task created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

 
    @staticmethod
    async def get_all_tasks(session: AsyncSession) -> list[TasksOut]:
        all_tasks = await tasks.TaskDao(session).get_all()
        return [TasksOut.model_validate(_task) for _task in all_tasks]

    @staticmethod
    async def task_name_exists(session: AsyncSession, name: str) -> TasksModel | None:
        _task = await tasks.TaskDao(session).get_by_name(name)
        return _task if _task else None

    @staticmethod
    async def get_task_by_id(task_id: int, session: AsyncSession) -> TasksOut:
        _task = await tasks.TaskDao(session).get_by_id(task_id)
        if not _task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task with the given id does not exist!!!",
            )
        return TasksOut.model_validate(_task)
    
    
    @staticmethod
    async def count_tasks(session: AsyncSession, user_id:int):
        _task = await tasks.TaskDao(session).count_tasks(user_id)
        _pending = await tasks.TaskDao(session).count_pending_tasks(user_id)
        _achievements = await tasks.TaskDao(session).count_achievement(user_id)
       
        achievements = await achievement.AchievementDao(session).get_achievement_by_user_id(user_id)

        total_points = 0
        
        for point in achievements:
            total_points += point.points_reward
            
            
        result = {
            "total_task": _task,
            "achievements": _achievements,
            "pending": _pending,
            "count_rewards": total_points
        }
        return result
    
    
    @staticmethod
    async def pie_chart_metrics(session: AsyncSession, user_id:int):
        _task = await tasks.TaskDao(session).count_tasks(user_id)
        _pending = await tasks.TaskDao(session).count_pending_tasks(user_id)
            
        result = []
        result.append(["Pending","Completed"])
        result.append([_pending,_task ])
        return result
    
    @staticmethod
    async def get_tasks_by_user_id(user_id: int,session: AsyncSession) -> list[TasksOut]:
        all_tasks = await tasks.TaskDao(session).get_tasks_by_user_id(user_id)
        return [TasksOut.model_validate(_task) for _task in all_tasks]

    @staticmethod
    async def delete_task_by_id(task_id: int, session: AsyncSession):
        _task = await tasks.TaskDao(session).delete_by_id(task_id)
        if not _task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Task deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
    
    @staticmethod
    async def change_task_status(
       task_data: TasksUpdate, session: AsyncSession
    ):

        task_exist = await  tasks.TaskDao(session).get_by_id(task_data.task_id)

        if not task_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task does not exist !!!",
            )
            
        task_exist.completed_date = datetime.now()
        
        if task_data.status == True:
        
            original_datetime_str = str(task_exist.created_at)

            # Convert string to datetime object
            original_datetime_object = datetime.strptime(original_datetime_str, "%Y-%m-%d %H:%M:%S.%f")

            # Convert datetime object to a string with the desired format
            formatted_datetime_str = original_datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        
            points = calculate_reward(formatted_datetime_str)

            if points >0:
                delayed = False
            else: 
                delayed = True
 
            result_model = {
                "achievement_date" : datetime.now(),
                "user_id" : task_exist.user_id,
                "delayed": delayed,
                "achievement_details": f"Completed : {task_exist.task_name}",
                "points_reward" : points
            }
        
            achievement = await AchievementService.create_achievement(result_model, session)
            print(achievement)
            logger.info(f"Achievement successfully updated: {achievement}!!!")
            
        logger.info(f"Tasks successfully updated: {task_exist}!!!")
        session.add(task_exist)
        await session.commit()
        
        return JSONResponse(
            content={"message": "Task successfully updated"},
            status_code=status.HTTP_201_CREATED,
        )
       
