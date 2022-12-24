from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Attempt])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tests.
    """
    if crud.user.is_superuser(current_user):
        tests = crud.attempt.get_multi(db, skip=skip, limit=limit)
    else:
        tests = crud.attempt.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return tests


class AttemptInput(BaseModel):
    tests: list[int]


@router.post("/")#, response_model=schemas.Attempt)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: AttemptInput,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new test.
    """
    result = crud.attempt.create_attempt(db=db,
                                         attempts=item_in.tests,
                                         owner_id=current_user.id,
                                         attempt_id=item_in.tests[0]**2 * current_user.id**3)
    return {"attempt_id": result.id}


@router.put("/{id}", response_model=schemas.Attempt)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.AttemptUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an Test.
    """
    test = crud.attempt.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    test = crud.attempt.update(db=db, db_obj=test, obj_in=item_in)
    return test


@router.get("/{id}", response_model=schemas.Attempt)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get test by ID.
    """
    test = crud.attempt.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return test


@router.delete("/{id}", response_model=schemas.Attempt)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    test_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an Test.
    """
    test = crud.attempt.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    test = crud.attempt.remove(db=db, id=id, test_id=test_id)
    return test
