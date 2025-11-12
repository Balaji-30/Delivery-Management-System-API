from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseService:
    def __init__(self,model: SQLModel, session: AsyncSession):
        # Database session to be used in service methods
        self.session = session
        # Model class to be used in service methods
        self.model = model

    async def _get(self, id: UUID):
        return await self.session.get(self.model, id)
    
    async def _add(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def _update(self, entity: SQLModel):
        return await self._add(entity)
    
    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)
        await self.session.commit()