from typing import Generic, TypeVar, Optional, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from services.database import Base
from pydantic import BaseModel
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)
CreateType = TypeVar("CreateType", bound=BaseModel)
UpdateType = TypeVar("UpdateType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateType, UpdateType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: AsyncSession, body: CreateType) -> ModelType:
        obj = self.model(**body.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def retrieve(self, db: AsyncSession, id: str | int) -> Optional[ModelType]:
        stat = select(self.model).filter(self.model.id == id)
        result = await db.execute((stat))
        return result.scalars().first()

    async def list(
        self,
        db: AsyncSession,
        query: Any = None,
        order_by: Any = None,
        limit: int = 10,
        page: int = 1,
    ) -> list[ModelType]:
        stat = select(self.model)
        if query:
            stat.filter(query)

        if order_by:
            stat.order_by(order_by)

        if limit and page:
            offset = (page - 1) * limit
            stat.offset(offset).limit(limit)

        result = await db.execute(stat)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateType
    ) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
