import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class TestBase(BaseModel):
    errors: Optional[str] = None
    choosed_number: Optional[str] = None
    time: Optional[int] = None
    table_id: Optional[int] = None


# Properties to receive on item creation
class TestCreate(TestBase):
    errors: str
    choosed_number: str
    time: int
    table_id: int


# Properties to receive on item update
class TestUpdate(TestBase):
    pass


# Properties shared by models stored in DB
class TestInDBBase(TestBase):
    id: int
    owner_id: int
    created: datetime.datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Test(TestInDBBase):
    pass


# Properties properties stored in DB
class TestInDB(TestInDBBase):
    pass
