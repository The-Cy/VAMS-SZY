from database.db import SessionLocal

from database.models import (
    Course,
    Lecturer
)



# =====================================
# LOAD COURSES
# =====================================

def get_courses():

    db = SessionLocal()


    courses = db.query(
        Course
    ).all()


    data = []


    for course in courses:

        data.append({

            "id": course.id,

            "name": course.course_name,

            "code": course.course_code

        })


    db.close()


    return data





# =====================================
# LOAD LECTURERS
# =====================================

def get_lecturers():

    db = SessionLocal()


    lecturers = db.query(
        Lecturer
    ).all()


    data = []


    for lecturer in lecturers:

        data.append({

            "id": lecturer.id,

            "name": lecturer.full_name

        })


    db.close()


    return data