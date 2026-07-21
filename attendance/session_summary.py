from database.db import SessionLocal

from database.models import (
    Student,
    AttendanceRecord,
    AttendanceSession,
    StudentCourse
)



def get_session_summary(session_id):

    db = SessionLocal()


    session = db.query(
        AttendanceSession
    ).filter(
        AttendanceSession.id == session_id
    ).first()



    if not session:

        db.close()

        return None



    # Get registered students
    students = (

        db.query(Student)

        .join(
            StudentCourse,
            Student.id == StudentCourse.student_id
        )

        .filter(
            StudentCourse.course_id == session.course_id
        )

        .all()

    )



    present = []

    absent = []



    for student in students:


        record = db.query(
            AttendanceRecord
        ).filter(

            AttendanceRecord.session_id == session_id,

            AttendanceRecord.student_id == student.id

        ).first()



        data = {

            "name": student.full_name,

            "student_number": student.student_number,

            "status":
                record.status
                if record
                else "Absent"

        }



        if data["status"] == "Present":

            present.append(data)

        else:

            absent.append(data)



    db.close()



    return {

        "session_id": session_id,

        "course_id": session.course_id,

        "present_count": len(present),

        "absent_count": len(absent),

        "total_students": len(students),

        "present": present,

        "absent": absent

    }