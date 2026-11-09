from api import (application, category, course, enrollment, study_group,user,)


from database.db import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CourseraFastapi",
    description=(
        "API for managing users, courses, study groups, applications, and"
        " enrollments."
    ),
    version="1.0.0",
)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(course.router)
app.include_router(study_group.router)
app.include_router(application.router)
app.include_router(enrollment.router)


@app.get("/")
def root():
  return {
      "message": "Welcome to the LMS API! Project is running successfully."
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)