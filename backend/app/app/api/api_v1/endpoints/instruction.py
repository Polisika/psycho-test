from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.Instructions)
def read_items(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve items.
    """
    try:
        instruction = crud.instruction.get(db, 1)
    except:
        instruction = \
            crud.instruction.create_with_owner(db=db,
                                               obj_in=schemas.InstructionsCreate(
                                                   description="The first rule - the table should be at a distance of "
                                                               "30-35 cm from the eyes. At the same time, it must be "
                                                               "raised at a small angle. Next, you should focus your "
                                                               "gaze in the center of the card - it is forbidden to take "
                                                               "his eyes to the sides, so the desired effect will not be "
                                                               "achieved.@@Average error num: @@Work warming-up: @@The "
                                                               "result of 1,0 and lower shows good warming-up, while 1,0 "
                                                               "and more means\n that one needs more time to prepare for "
                                                               "the main work (warm-up).@@Psychological stability: @@The "
                                                               "result of 1,0 and less shown good psychological stability. "
                                                               "Positive\n effects include attention stability, improved "
                                                               "visual perception, improved\n peripheral vision, and "
                                                               "development of speed reading."),
                                               owner_id=1)
    return instruction


@router.post("/", response_model=schemas.Instructions)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.InstructionsCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.instruction.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{id}", response_model=schemas.Instructions)
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        item_in: schemas.InstructionsUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.instruction.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.instruction.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{id}", response_model=schemas.Instructions)
def delete_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.instruction.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.remove(db=db, id=id)
    return item
