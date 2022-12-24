import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class AttemptBase(BaseModel):
    test_id: Optional[int] = None


# Properties to receive on item creation
class AttemptCreate(AttemptBase):
    test_id: int


# Properties to receive on item update
class AttemptUpdate(AttemptBase):
    pass


# Properties shared by models stored in DB
class AttemptInDBBase(AttemptBase):
    id: int
    owner_id: int
    created: datetime.datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Attempt(AttemptInDBBase):
    pass


# Properties properties stored in DB
class AttemptInDB(AttemptInDBBase):
    pass
