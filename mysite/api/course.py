from database.db import get_db
from database.models import Course
from database.schema import CourseCreate, CourseResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/course", tags=["Course"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
  new_course = Course(**course.model_dump())
  db.add(new_course)
  db.commit()
  db.refresh(new_course)
  return new_course


@router.get("/", response_model=list[CourseResponse])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return db.query(Course).offset(skip).limit(limit).all()


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
  course = db.query(Course).filter(Course.id == course_id).first()
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")
  return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int, course: CourseCreate, db: Session = Depends(get_db)
):
  db_course = db.query(Course).filter(Course.id == course_id).first()
  if not db_course:
    raise HTTPException(status_code=404, detail="Course not found")

  for key, value in course.model_dump().items():
    setattr(db_course, key, value)

  db.commit()
  db.refresh(db_course)
  return db_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
  db_course = db.query(Course).filter(Course.id == course_id).first()
  if not db_course:
    raise HTTPException(status_code=404, detail="Course not found")

  db.delete(db_course)
  db.commit()
  return None