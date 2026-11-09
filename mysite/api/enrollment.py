from database.db import get_db
from database.models import Enrollment
from database.schema import EnrollmentCreate, EnrollmentResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post(
    "/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
  new_enrollment = Enrollment(**enrollment.dict())
  db.add(new_enrollment)
  db.commit()
  db.refresh(new_enrollment)
  return new_enrollment


@router.get("/", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
  return db.query(Enrollment).all()