from database.db import get_db
from database.models import Application
from database.schema import ApplicationCreate, ApplicationResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/application", tags=["Application"])


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)

def create_application(app_data: ApplicationCreate, db: Session = Depends(get_db)):
  new_app = Application(**app_data.model_dump())
  db.add(new_app)
  db.commit()
  db.refresh(new_app)
  return new_app


@router.get("/", response_model=list[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
  return db.query(Application).all()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
  app_obj = db.query(Application).filter(Application.id == application_id).first()
  if not app_obj:
    raise HTTPException(status_code=404, detail="Application not found")
  return app_obj


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    app_data: ApplicationCreate,
    db: Session = Depends(get_db),):

  db_app = db.query(Application).filter(Application.id == application_id).first()
  if not db_app:
    raise HTTPException(status_code=404, detail="Application not found")

  for key, value in app_data.model_dump().items():
    setattr(db_app, key, value)

  db.commit()
  db.refresh(db_app)
  return db_app


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
  db_app = db.query(Application).filter(Application.id == application_id).first()
  if not db_app:
    raise HTTPException(status_code=404, detail="Application not found")

  db.delete(db_app)
  db.commit()
  return None