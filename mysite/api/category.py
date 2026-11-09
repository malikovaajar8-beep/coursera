from database.db import get_db
from database.models import Category
from database.schema import CategoryCreate, CategoryResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
  db_category = (
      db.query(Category)
      .filter(Category.category_name == category.category_name)
      .first()
  )
  if db_category:
    raise HTTPException(status_code=400, detail="Category already exists")

  new_category = Category(**category.model_dump())
  db.add(new_category)
  db.commit()
  db.refresh(new_category)
  return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
  return db.query(Category).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
  category = db.query(Category).filter(Category.id == category_id).first()
  if not category:
    raise HTTPException(status_code=404, detail="Category not found")
  return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, category: CategoryCreate, db: Session = Depends(get_db)
):
  db_category = db.query(Category).filter(Category.id == category_id).first()
  if not db_category:
    raise HTTPException(status_code=404, detail="Category not found")

  for key, value in category.model_dump().items():
    setattr(db_category, key, value)

  db.commit()
  db.refresh(db_category)
  return db_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
  db_category = db.query(Category).filter(Category.id == category_id).first()
  if not db_category:
    raise HTTPException(status_code=404, detail="Category not found")

  db.delete(db_category)
  db.commit()
  return None