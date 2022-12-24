from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Test])
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
        tests = crud.test.get_multi(db, skip=skip, limit=limit)
    else:
        tests = crud.test.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return tests


@router.post("/", response_model=schemas.Test)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.TestCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new test.
    """
    test = crud.test.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return test


@router.put("/{id}", response_model=schemas.Test)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.TestUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an Test.
    """
    test = crud.test.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    test = crud.test.update(db=db, db_obj=test, obj_in=item_in)
    return test


@router.get("/{id}", response_model=schemas.Test)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get test by ID.
    """
    test = crud.test.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return test


@router.delete("/{id}", response_model=schemas.Test)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an Test.
    """
    test = crud.test.get(db=db, id=id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not crud.user.is_superuser(current_user) and (test.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    test = crud.test.remove(db=db, id=id)
    return test
