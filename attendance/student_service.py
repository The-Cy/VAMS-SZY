from database.db import SessionLocal
from database.models import Student


# -------------------------
# ADD STUDENT
# -------------------------
def add_student(full_name, index_number, programme, year_of_study):
    db = SessionLocal()

    student = Student(
        full_name=full_name,
        index_number=index_number,
        programme=programme,
        year_of_study=year_of_study
    )

    db.add(student)
    db.commit()
    db.close()


# -------------------------
# GET ALL STUDENTS
# -------------------------
def get_all_students():
    db = SessionLocal()

    students = db.query(Student).all()

    db.close()
    return students


# -------------------------
# DELETE STUDENT
# -------------------------
def delete_student(index_number):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.index_number == index_number
    ).first()

    if student:
        db.delete(student)
        db.commit()

    db.close()