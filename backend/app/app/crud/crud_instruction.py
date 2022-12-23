from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.instruction import Instruction
from app.schemas.instructions import InstructionsCreate, InstructionsUpdate


class CRUDItem(CRUDBase[Instruction, InstructionsCreate, InstructionsUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: InstructionsCreate, owner_id: int
    ) -> Instruction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int
    ) -> List[Instruction]:
        return (
            db.query(self.model)
            .filter(Instruction.owner_id == owner_id)
            .all()
        )


instruction = CRUDItem(Instruction)
