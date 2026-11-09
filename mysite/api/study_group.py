from database.db import get_db
from database.models import StudyGroup
from database.schema import StudyGroupCreate, StudyGroupResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/group", tags=["Study Group"])


@router.post(
    "/", response_model=StudyGroupResponse, status_code=status.HTTP_201_CREATED
)
def create_study_group(group: StudyGroupCreate, db: Session = Depends(get_db)):
  new_group = StudyGroup(**group.model_dump())
  db.add(new_group)
  db.commit()
  db.refresh(new_group)
  return new_group


@router.get("/", response_model=list[StudyGroupResponse])
def get_study_groups(db: Session = Depends(get_db)):
  return db.query(StudyGroup).all()


@router.get("/{group_id}", response_model=StudyGroupResponse)
def get_study_group(group_id: int, db: Session = Depends(get_db)):
  group = db.query(StudyGroup).filter(StudyGroup.id == group_id).first()
  if not group:
    raise HTTPException(status_code=404, detail="Study Group not found")
  return group


@router.put("/{group_id}", response_model=StudyGroupResponse)
def update_study_group(
    group_id: int, group: StudyGroupCreate, db: Session = Depends(get_db)
):
  db_group = db.query(StudyGroup).filter(StudyGroup.id == group_id).first()
  if not db_group:
    raise HTTPException(status_code=404, detail="Study Group not found")

  for key, value in group.model_dump().items():
    setattr(db_group, key, value)

  db.commit()
  db.refresh(db_group)
  return db_group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study_group(group_id: int, db: Session = Depends(get_db)):
  db_group = db.query(StudyGroup).filter(StudyGroup.id == group_id).first()
  if not db_group:
    raise HTTPException(status_code=404, detail="Study Group not found")

  db.delete(db_group)
  db.commit()
  return None