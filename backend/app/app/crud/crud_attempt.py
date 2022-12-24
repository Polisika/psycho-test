from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate, AttemptUpdate


class CRUDItem(CRUDBase[Attempt, AttemptCreate, AttemptUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AttemptCreate, owner_id: int, attempt_id: int
    ) -> Attempt:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id, id=attempt_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_attempt(self, db: Session, *, attempts: list[int], owner_id: int, attempt_id: int) -> Attempt:
        assert len(attempts) > 0
        db_obj_c = None
        for _id in attempts:
            m = AttemptCreate(test_id=_id)
            obj_in_data = jsonable_encoder(m)
            db_obj_c = self.model(**obj_in_data, owner_id=owner_id, id=attempt_id)
            db.add(db_obj_c)
        assert db_obj_c
        db.commit()
        db.refresh(db_obj_c)
        return db_obj_c

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Attempt]:
        return (
            db.query(self.model)
            .filter(Attempt.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


attempt = CRUDItem(Attempt)
