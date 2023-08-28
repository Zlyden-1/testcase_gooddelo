from uuid import uuid4
from pydantic import BaseModel, Field, UUID4


class EntryModel(BaseModel):
    uuid: UUID4 = Field(default_factory=uuid4)
    text: str = Field(...)
