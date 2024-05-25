from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate


router_operation = APIRouter(
    prefix='/operations',
    tags=['Operation'],
)


@router_operation.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    result = result.mappings().all()

    # Преобразование результатов в список словарей
    operations_list = [dict(row) for row in result]

    return operations_list


@router_operation.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()

    return {'status': 'success'}
