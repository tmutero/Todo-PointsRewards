from app.models.role import Role
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao


class RoleDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, role_data) -> Role:
        _role = Role(**role_data)
        self.session.add(_role)
        await self.session.commit()
        await self.session.refresh(_role)
        return _role

    async def get_by_id(self, role_id: int) -> Role | None:
        statement = select(Role).where(Role.id == role_id)
        return await self.session.scalar(statement=statement)


    async def get_all(self) -> list[Role]:
        statement = select(Role).order_by(Role.id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Role))
        await self.session.commit()

    async def delete_by_id(self, role_id: int) -> Role | None:
        _role = await self.get_by_id(role_id=role_id)
        statement = delete(Role).where(Role.id == role_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _role
    
    async def get_by_name(self, name) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return await self.session.scalar(statement=statement)
