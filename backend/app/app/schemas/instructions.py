from typing import Optional

from pydantic import BaseModel


# Shared properties
class InstructionsBase(BaseModel):
    description: Optional[str] = None


# Properties to receive on item creation
class InstructionsCreate(InstructionsBase):
    description: str


# Properties to receive on item update
class InstructionsUpdate(InstructionsBase):
    pass


# Properties shared by models stored in DB
class InstructionsInDBBase(InstructionsBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Instructions(InstructionsInDBBase):
    pass


# Properties stored in DB
class InstructionsInDB(InstructionsInDBBase):
    pass
