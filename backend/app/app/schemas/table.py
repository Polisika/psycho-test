from typing import Optional

from pydantic import BaseModel


# Shared properties
class TableBase(BaseModel):
    digits: Optional[str] = None


# Properties to receive on item creation
class TableCreate(TableBase):
    digits: str


# Properties to receive on item update
class TableUpdate(TableBase):
    pass


# Properties shared by models stored in DB
class TableInDBBase(TableBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Table(TableInDBBase):
    pass


# Properties properties stored in DB
class TableInDB(TableInDBBase):
    pass
