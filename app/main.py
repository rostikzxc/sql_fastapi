from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from database import SessionLocal, Base, engine
from schemas import (
    UserCreate,
    UserUpdate,
    StudentCreate,
    CourseCreate,
    CommentCreate,
    ProfileCreate
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


# -----------------------
# DB dependency
# -----------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Profile
# -----------------------

@app.post("/profile")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(profile.user_id, profile.name, db)

# -----------------------
# Test endpoint
# -----------------------


@app.post("/comments")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(comment.user_id, comment.text, db)


# -----------------------
# User routes
# -----------------------

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user, db)


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(user_id, db)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(user_id, user, db)


@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return crud.patch_user(user_id, user, db)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(user_id, db)


# -----------------------
# Student routes
# -----------------------

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(student, db)


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student(student_id, db)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    return crud.update_student(student_id, student, db)


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return crud.delete_student(student_id, db)


# -----------------------
# Course routes
# -----------------------

@app.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(course, db)


@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)


# -----------------------
# Relationship routes
# -----------------------

@app.post("/student-course")
def add_student_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    return crud.add_student_to_course(student_id, course_id, db)