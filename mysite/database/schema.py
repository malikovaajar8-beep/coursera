from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
  full_name: str
  email: EmailStr
  role: str = "student"
  user_status: str = "free"


class UserCreate(UserBase):
  password: str


class UserResponse(UserBase):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


# --- Category Schemas ---
class CategoryBase(BaseModel):
  category_name: str


class CategoryCreate(CategoryBase):
  pass


class CategoryResponse(CategoryBase):
  id: int

  class Config:
    from_attributes = True


# --- Course Schemas ---
class CourseBase(BaseModel):
  title: str
  category_id: int
  description: Optional[str] = None
  level: str = "beginner"
  price: float = 0.0
  duration_weeks: int
  is_active: bool = True
  status: str = "free"


class CourseCreate(CourseBase):
  pass


class CourseResponse(CourseBase):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


# --- StudyGroup Schemas ---
class StudyGroupBase(BaseModel):
  name: str
  course_id: int
  teacher_id: Optional[int] = None
  starts_on: Optional[datetime] = None
  ends_on: Optional[datetime] = None
  status: str = "recruiting"


class StudyGroupCreate(StudyGroupBase):
  pass


class StudyGroupResponse(StudyGroupBase):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


# --- Application Schemas ---
class ApplicationBase(BaseModel):
  course_id: int
  comment: Optional[str] = None


class ApplicationCreate(ApplicationBase):
  student_id: int


class ApplicationResponse(ApplicationBase):
  id: int
  student_id: int
  manager_id: Optional[int] = None
  status: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True


# --- Enrollment Schemas ---
class EnrollmentBase(BaseModel):
  student_id: int
  group_id: int


class EnrollmentCreate(EnrollmentBase):
  pass


class EnrollmentResponse(EnrollmentBase):
  id: int
  status: str
  created_at: datetime

  class Config:
    from_attributes = True