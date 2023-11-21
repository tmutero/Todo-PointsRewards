from app.schemas.role import RoleIn, RoleOut
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role as RoleModel

from app.daos import role


class RoleService:
    @staticmethod
    async def create_role(role_data: RoleIn, session: AsyncSession):
        role_exist = await RoleService.role_name_exists(session, role_data.name)

        if role_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with the given name already exists!!!",
            )

        new_role = await role.RoleDao(session).create(role_data.model_dump())
        logger.info(f"New role created successfully: {new_role}!!!")
        return JSONResponse(
            content={"message": "Role created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

 
    @staticmethod
    async def get_all_roles(session: AsyncSession) -> list[RoleOut]:
        all_roles = await role.RoleDao(session).get_all()
        return [RoleOut.model_validate(_role) for _role in all_roles]

    @staticmethod
    async def role_name_exists(session: AsyncSession, name: str) -> RoleModel | None:
        _user = await role.RoleDao(session).get_by_name(name)
        return _user if _user else None

    @staticmethod
    async def get_role_by_id(role_id: int, session: AsyncSession) -> RoleOut:
        _role = await role.RoleDao(session).get_by_id(role_id)
        if not _role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role with the given id does not exist!!!",
            )
        return RoleOut.model_validate(_role)

    @staticmethod
    async def delete_role_by_id(role_id: int, session: AsyncSession):
        _role = await role.RoleDao(session).delete_by_id(role_id)
        if not _role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Role deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
        
