from database.db import SessionLocal
from database.models import Course, Lecturer



# =====================================
# GET COURSES
# =====================================

def get_courses():

    db = SessionLocal()


    courses = db.query(
        Course
    ).all()


    result = []


    for course in courses:

        result.append({

            "id": course.id,

            "code": course.course_code,

            "name": course.course_name

        })


    db.close()


    return result





# =====================================
# GET LECTURERS
# =====================================

def get_lecturers():

    db = SessionLocal()


    lecturers = db.query(
        Lecturer
    ).all()


    result = []


    for lecturer in lecturers:

        result.append({

            "id": lecturer.id,

            "name": lecturer.full_name

        })


    db.close()


    return result