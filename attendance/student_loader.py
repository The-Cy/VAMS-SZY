from database.db import SessionLocal

from database.models import (
    Student,
    StudentCourse
)



# =====================================
# GET STUDENTS REGISTERED FOR COURSE
# =====================================

def get_course_students(course_id):

    db = SessionLocal()


    students = (
        db.query(Student)
        .join(
            StudentCourse,
            Student.id == StudentCourse.student_id
        )
        .filter(
            StudentCourse.course_id == course_id
        )
        .all()
    )


    result = []


    for student in students:

        result.append(

            {
                "id": student.id,

                "name": student.full_name,

                "student_number":
                    student.student_number
            }

        )


    db.close()


    return result