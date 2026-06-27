from sqlalchemy.orm import Session

from app.models import User, Student, Course, Comment, Profile
from app.schemas import UserCreate, UserUpdate, StudentCreate, CourseCreate


# -----------------------
# Helpers
# -----------------------

def get_by_id(model, obj_id: int, db: Session):
    return db.query(model).filter(model.id == obj_id).first()

# -----------------------
# Profile
# -----------------------

def create_profile(user_id: int, name:str, db: Session):
    user = get_by_id(User, user_id, db)

    if not user:
        return None
    
    profile = Profile(user_id=user.id, name=name)

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

# -----------------------
# Comments
# -----------------------

def create_comment(user_id: int, text: str, db: Session):
    user = get_by_id(User, user_id, db)

    if not user:
        return None

    comment = Comment(text=text, user=user)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# -----------------------
# Students <-> Courses
# -----------------------

def add_student_to_course(student_id: int, course_id: int, db: Session):
    student = get_by_id(Student, student_id, db)
    course = get_by_id(Course, course_id, db)

    if not student or not course:
        return None

    if course not in student.courses:
        student.courses.append(course)

    db.commit()
    db.refresh(student)

    return student


# -----------------------
# Users
# -----------------------

def get_users(db: Session):
    return db.query(User).all()


def get_user(user_id: int, db: Session):
    return get_by_id(User, user_id, db)


def create_user(user: UserCreate, db: Session):
    db_user = User(name=user.name)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(user_id: int, user: UserCreate, db: Session):
    db_user = get_by_id(User, user_id, db)

    if not db_user:
        return None

    db_user.name = user.name

    db.commit()
    db.refresh(db_user)

    return db_user


def patch_user(user_id: int, user: UserUpdate, db: Session):
    db_user = get_by_id(User, user_id, db)

    if not db_user:
        return None

    if user.name is not None:
        db_user.name = user.name

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(user_id: int, db: Session):
    db_user = get_by_id(User, user_id, db)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user


# -----------------------
# Students
# -----------------------

def create_student(student: StudentCreate, db: Session):
    db_student = Student(name=student.name)

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_students(db: Session):
    return db.query(Student).all()


def get_student(student_id: int, db: Session):
    return get_by_id(Student, student_id, db)


def update_student(student_id: int, student: StudentCreate, db: Session):
    db_student = get_by_id(Student, student_id, db)

    if not db_student:
        return None

    db_student.name = student.name

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(student_id: int, db: Session):
    db_student = get_by_id(Student, student_id, db)

    if not db_student:
        return None

    db.delete(db_student)
    db.commit()

    return db_student


# -----------------------
# Courses
# -----------------------

def create_course(course: CourseCreate, db: Session):
    db_course = Course(name=course.name)

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_courses(db: Session):
    return db.query(Course).all()