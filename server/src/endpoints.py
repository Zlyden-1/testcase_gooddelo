from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Body, Path, Response
from fastapi.exceptions import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from fastapi_cache.decorator import cache
from pydantic import UUID4

from database import get_async_session
from models import entrie
from schemas import EntryModel

router = APIRouter(tags=["Entries"])


@router.get("/all")
@cache(expire=30)
async def get_all_entries(session: AsyncSession = Depends(get_async_session)):
    query = select(entrie)
    result = await session.execute(query)
    return [EntryModel(uuid=i.uuid, text=i.text) for i in result.all()]


@router.post("/new")
async def add_new_entry(
    text: str = Body(embed=True),
    session: AsyncSession = Depends(get_async_session),
):
    new_entry = EntryModel(text=text)
    stmt = insert(entrie).values(**new_entry.dict())
    await session.execute(stmt)
    await session.commit()
    return Response(status_code=201)


@router.get("/entry/{uuid}")
async def get_entry(
    uuid: UUID4,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(entrie).where(entrie.c.uuid == uuid)
    result = (await session.execute(query)).one_or_none()
    if result:
        return EntryModel(uuid=result.uuid, text=result.text)
    else:
        raise HTTPException(status_code=404, detail="No entry with such uuid found")


@router.get("/entries/{count}")
async def get_certain_number_of_entries_with_optional_offset(
    count: Annotated[int, Path(ge=0)],
    offset: Optional[int] = 0,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(entrie).limit(count).offset(offset)
    result = await session.execute(query)
    return [EntryModel(uuid=i.uuid, text=i.text) for i in result.all()]


@router.get("/by_filters")
@cache(expire=30)
async def get_entries_by_filters(
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    session: AsyncSession = Depends(get_async_session),
):
    if end_datetime is None:
        end_datetime = datetime.now()
    if not start_datetime:
        query = select(entrie).where(entrie.c.creation_datetime <= end_datetime)
    else:
        if end_datetime < start_datetime:
            raise HTTPException(status_code=422, detail="Start date must be less than end date")
        query = (
            select(entrie)
            .where(entrie.c.creation_datetime <= end_datetime)
            .where(entrie.c.creation_datetime >= start_datetime)
        )
    result = await session.execute(query)
    return [EntryModel(uuid=i.uuid, text=i.text) for i in result.all()]


@router.put("/update/{uuid}")
async def update_entry(
    uuid: UUID4,
    entry: EntryModel = Body(embed=True),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = update(entrie).where(entrie.c.uuid == uuid).values(text=entry.text)
    await session.execute(stmt)
    await session.commit()
    return


@router.delete("/{uuid}")
async def delete_entry(
    uuid: UUID4,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = delete(entrie).where(entrie.c.uuid == uuid)
    await session.execute(stmt)
    await session.commit()
    return Response(status_code=204)
