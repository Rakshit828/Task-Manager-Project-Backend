from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import CreateTaskSchema, UpdateTaskSchema, ResponseTaskSchema
from .service import book_service_provider
from .models import Tasks
from uuid import UUID
from typing import List


task_router = APIRouter()

@task_router.get('/', response_model=List[ResponseTaskSchema])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await book_service_provider.get_all_tasks(session)
    return result


@task_router.get('/{uuid}')
async def get_a_task(uuid: UUID, session: AsyncSession = Depends(get_session)):
    result = await book_service_provider.get_a_task(uuid, session)
    return result 


@task_router.post('/create', response_model=ResponseTaskSchema)
async def create_task(task: CreateTaskSchema, session: AsyncSession = Depends(get_session)):
    try:
        result = await book_service_provider.add_taks(task, session) 
        return result
    except Exception as e:
        return e


@task_router.delete('/delete/{uuid}', response_model=ResponseTaskSchema)
async def delete_task(uuid: UUID, session: AsyncSession = Depends(get_session)):
    try:
        result = await book_service_provider.delete_task(uuid, session) 
        print(result)
        return result.model_dump()
    except Exception as e:
        return e


@task_router.put('/update/{uuid}', response_model=ResponseTaskSchema)
async def update_task(uuid: UUID, task_details: UpdateTaskSchema, session: AsyncSession = Depends(get_session)):
    print(task_details)
    result = await book_service_provider.update_task(uuid, task_details, session)
    return result.model_dump()

