from datetime import datetime
from sqlalchemy import (Boolean,Column,DateTime,Enum,Float,ForeignKey,Integer, String, Text,)
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  role = Column(Enum("student", "teacher", "manager", "admin", name="user_role"), default="student",)
  user_status = Column( Enum("free", "pro", name="user_status_type"), default="free")
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  applications = relationship("Application", back_populates="student")
  enrollments = relationship("Enrollment", back_populates="student")
  study_groups = relationship("StudyGroup", back_populates="teacher")


class Category(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  category_name = Column(String, unique=True, nullable=False)
  courses = relationship("Course", back_populates="category_rel")


class Course(Base):
  __tablename__ = "courses"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
  description = Column(Text, nullable=True)
  level = Column( Enum("beginner", "intermediate", "advanced", name="course_level"), default="beginner",)
  price = Column(Float, default=0.0)
  duration_weeks = Column(Integer, nullable=False)
  is_active = Column(Boolean, default=True)
  status = Column( Enum("free", "plus", name="course_status_type"), default="free")
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )
  category_rel = relationship("Category", back_populates="courses")
  study_groups = relationship("StudyGroup", back_populates="course")
  applications = relationship("Application", back_populates="course")


class StudyGroup(Base):
  __tablename__ = "study_groups"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
  teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
  starts_on = Column(DateTime, nullable=True)
  ends_on = Column(DateTime, nullable=True)
  status = Column(Enum( "recruiting","active","completed", "cancelled",name="group_status_type",)
                  ,default="recruiting",)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  course = relationship("Course", back_populates="study_groups")
  teacher = relationship("User", back_populates="study_groups")
  enrollments = relationship("Enrollment", back_populates="group")


class Application(Base):
  __tablename__ = "applications"

  id = Column(Integer, primary_key=True, index=True)
  student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
  manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
  comment = Column(Text, nullable=True)
  status = Column( Enum( "new","in_progress", "accepted", "rejected","cancelled", name="application_status_type",),
                   default="new",)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  student = relationship("User", foreign_keys=[student_id], back_populates="applications")
  course = relationship("Course", back_populates="applications")


class Enrollment(Base):
  __tablename__ = "enrollments"

  id = Column(Integer, primary_key=True, index=True)
  student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
  status = Column(Enum("active","completed",  "cancelled", name="enrollment_status_type",), default="active",)
  created_at = Column(DateTime, default=datetime.utcnow)
  student = relationship("User", back_populates="enrollments")
  group = relationship("StudyGroup", back_populates="enrollments")