from app.models.permission import Permission
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao

class PermissionDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, permission_data) -> Permission:
        _permission = Permission(**permission_data)
        self.session.add(_permission)
        await self.session.commit()
        await self.session.refresh(_permission)
        return _permission

    async def get_by_id(self, permission_id: int) -> Permission | None:
        statement = select(Permission).where(Permission.permission_id == permission_id)
        return await self.session.scalar(statement=statement)


    async def get_all(self) -> list[Permission]:
        statement = select(Permission).order_by(Permission.permission_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Permission))
        await self.session.commit()

    async def delete_by_id(self, permission_id: int) -> Permission | None:
        _permission = await self.get_by_id(permission_id=permission_id)
        statement = delete(Permission).where(Permission.id == permission_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _permission
    
    
    async def get_by_permission_by_user_role(self, user_id, role_id) -> Permission | None:
        statement = select(Permission).where(Permission.user_id == user_id and Permission.role_id == role_id)
        return await self.session.scalar(statement=statement)
    
    
    async def get_permissions_by_user_id(self, user_id: int)-> list[Permission]:
        statement = select(Permission).where(Permission.user_id == user_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
