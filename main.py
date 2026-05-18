from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.Studentcreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    return crud.get_student(db)

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.Studentcreate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student       

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)): 
    db_student = crud.delete_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}  