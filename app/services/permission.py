from app.schemas.permission import PermissionIn, PermissionOut
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission as PermissionModel

from app.daos import permission


class PermissionService:
    @staticmethod
    async def create_permissions(permission_data: PermissionIn, session: AsyncSession):
        permission_exist = await PermissionService.user_permissions_exists(session, permission_data.user_id, permission_data.role_id)

        if permission_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission with the given already exists!!!",
            )

        new_permission = await permission.PermissionDao(session).create(permission_data.model_dump())
        logger.info(f"New permission created successfully: {new_permission}!!!")
        return JSONResponse(
            content={"message": "Permission created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

 
    @staticmethod
    async def get_all_permissions(session: AsyncSession) -> list[PermissionOut]:
        all_permissions = await permission.PermissionDao(session).get_all()
        return [PermissionOut.model_validate(_role) for _role in all_permissions]

    @staticmethod
    async def user_permissions_exists(session: AsyncSession, user_id: int,role_id: int ) -> PermissionModel | None:
        _user_role = await permission.PermissionDao(session).get_by_permission_by_user_role(user_id,role_id )
        return _user_role if _user_role else None

    @staticmethod
    async def get_permissions_by_id(permissions_id: int, session: AsyncSession) -> PermissionOut:
        _permission = await permission.PermissionDao(session).get_by_id(permissions_id)
        if not _permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission with the given id does not exist!!!",
            )
        return PermissionOut.model_validate(_permission)

    @staticmethod
    async def delete_permission_by_id(role_id: int, session: AsyncSession):
        _permission = await permission.PermissionDao(session).delete_by_id(role_id)
        if not _permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Permission deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
        
    @staticmethod
    async def get_permissions_by_user_id(user_id: int,session: AsyncSession) -> list[PermissionOut]:
        all_permissions = await permission.PermissionDao(session).get_permissions_by_user_id(user_id)
        return [PermissionOut.model_validate(_task) for _task in all_permissions] 

