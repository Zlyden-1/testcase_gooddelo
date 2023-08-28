from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, Uuid, DateTime, create_engine
from database import DATABASE_URL

metadata = MetaData()

entrie = Table(
    "entrie",
    metadata,
    Column("uuid", Uuid, primary_key=True),
    Column("text", String, nullable=False),
    Column("creation_datetime", DateTime, nullable=False, default=datetime.now),
)

engine = create_engine(f"{DATABASE_URL}?async_fallback=True")
metadata.create_all(engine)
