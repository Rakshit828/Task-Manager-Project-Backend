from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from fastapi import status, HTTPException
from .schemas import CreateTaskSchema, UpdateTaskSchema
from .models import Tasks
from typing import List, Dict
from uuid import UUID


class BookService:
    async def get_all_tasks(self, session: AsyncSession) -> List[Dict]:
        statement = select(Tasks)
        result = await session.exec(statement)
        return result


    async def get_a_task(self, uuid: UUID, session: AsyncSession) -> Tasks:
        statement = select(Tasks).where(Tasks.task_uid == uuid)
        result = await session.exec(statement)
        result = result.first()
        return result


    async def add_taks(self, task: CreateTaskSchema, user_id: str, session: AsyncSession) -> Tasks:
        task_details = task.model_dump()
        new_task = Tasks(**task_details)
        new_task.user_id = user_id
        
        session.add(new_task)
        await session.commit()
        return new_task
    

    async def update_task(self, uuid: UUID, task_details: UpdateTaskSchema, session: AsyncSession) -> Tasks:
        result = await self.get_a_task(uuid, session)
        print(result)
        if not result:
            return None
        task_details_dict = task_details.model_dump(exclude_unset=True, exclude_defaults=True)
        print(task_details_dict)
        for key, value in task_details_dict.items():
            setattr(result, key, value)

        await session.commit()
        # We have to do session.commit() for any change in database
        return result
    

    async def delete_task(self, uuid: UUID, session: AsyncSession) -> Tasks:
        result = await self.get_a_task(uuid, session)
        if not result:
            return None
        
        await session.delete(result)
        await session.commit()

        return result
    

book_service_provider = BookService()