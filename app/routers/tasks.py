from app.schemas.tasks import TasksCount, TasksIn, TasksOut, TasksUpdate
from app.services.user import UserService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.token import Token
from app.services.tasks import TasksService

router = APIRouter(tags=["Task"], prefix="/task")


@router.post("/create_task", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TasksIn,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(UserService.get_current_user),
):
    return await TasksService.create_task(task_data, session)


@router.post("/update_task", status_code=status.HTTP_201_CREATED)
async def update_task(
    task_update: TasksUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(UserService.get_current_user),
):
    return await TasksService.change_task_status(task_update, session)


@router.get("/get_task_by_id/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(UserService.get_current_user),

) -> TasksOut:
    return await TasksService.get_task_by_id(task_id, session)

@router.get("/get_tasks_by_user_id/{user_id}", status_code=status.HTTP_200_OK)
async def get_tasks_by_user_id(
    user_id: int,
    current_user=Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session)
    ) -> list[TasksOut]:

    return await TasksService.get_tasks_by_user_id(user_id,session)


@router.get("/get_all_tasks", status_code=status.HTTP_200_OK)
async def get_all_tasks(session: AsyncSession = Depends(get_session),    
                        current_user=Depends(UserService.get_current_user),
                        ) -> list[TasksOut]:
    return await TasksService.get_all_tasks(session)


@router.delete("/delete_task_by_id/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task_by_id(
    task_id: int,
    current_user=Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await TasksService.delete_task_by_id(task_id, session)


@router.get("/report_tasks/{user_id}", status_code=status.HTTP_200_OK)
async def report_tasks(
    user_id: int,

    session: AsyncSession = Depends(get_session),
    # current_user=Depends(UserService.get_current_user),
):
    return await TasksService.count_tasks(session, user_id)

@router.get("/pie_chart_metrics/{user_id}", status_code=status.HTTP_200_OK)
async def pie_chart_metrics(
    user_id: int,

    session: AsyncSession = Depends(get_session),
    # current_user=Depends(UserService.get_current_user),
):
    return await TasksService.pie_chart_metrics(session, user_id)
