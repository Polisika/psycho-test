from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.table import Table
from app.schemas.test import TableCreate, TableUpdate


class CRUDItem(CRUDBase[Table, TableCreate, TableUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TableCreate, owner_id: int
    ) -> Table:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int
    ) -> List[Table]:
        return (
            db.query(self.model)
            .filter(Table.owner_id == owner_id)
            .all()
        )


table = CRUDItem(Table)
