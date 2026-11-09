from database.db import get_db
from database.models import User
from database.schema import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()
  if db_user:
    raise HTTPException(
        status_code=400, detail="Email already registered"
    )

  new_user = User(
      full_name=user.full_name,
      email=user.email,
      password=user.password,
      role=user.role,
      user_status=user.user_status,
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@router.get("/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = db.query(User).offset(skip).limit(limit).all()
  return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user