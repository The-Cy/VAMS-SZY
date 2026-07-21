from database.db import SessionLocal

from database.models import (
    Student,
    StudentCourse,
    AttendanceRecord
)



# ==========================================
# GET STUDENTS REGISTERED FOR COURSE
# ==========================================

def get_course_students(course_id, session_id=None):

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


        status = "Absent"



        # If attendance session exists,
        # check current status

        if session_id:


            record = db.query(
                AttendanceRecord
            ).filter(

                AttendanceRecord.session_id == session_id,

                AttendanceRecord.student_id == student.id

            ).first()



            if record:

                status = record.status



        result.append(

            {

                "student_id": student.id,

                "name": student.full_name,

                "student_number": student.student_number,

                "status": status

            }

        )



    db.close()


    return result