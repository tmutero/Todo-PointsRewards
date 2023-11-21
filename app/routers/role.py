from app.schemas.role import RoleIn, RoleOut
from app.services.user import UserService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.token import Token
from app.services.role import RoleService

router = APIRouter(tags=["Role"], prefix="/role")


@router.post("/create_role", status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleIn,
    session: AsyncSession = Depends(get_session),
):
    return await RoleService.create_role(role_data, session)


@router.get("/get_by_id/{role_id}", status_code=status.HTTP_200_OK)
async def get_role_by_id(
    role_id: int,
    current_user=Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RoleOut:
    return await RoleService.get_role_by_id(role_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_roles(session: AsyncSession = Depends(get_session),
                        current_user=Depends(UserService.get_current_user),
                        ) -> list[RoleOut]:
    return await RoleService.get_all_roles(session)


@router.delete("/delete_by_id/{role_id}", status_code=status.HTTP_200_OK)
async def delete_role_by_id(
    role_id: int,
    current_user=Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await RoleService.delete_role_by_id(role_id, session)
