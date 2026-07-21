from database.db import SessionLocal

from database.models import (
    AttendanceRecord,
    AttendanceSession,
    Student
)


# ======================================
# GET ATTENDANCE SUMMARY
# ======================================

def get_session_summary(session_id):

    db = SessionLocal()


    records = (

        db.query(
            AttendanceRecord,
            Student
        )

        .join(
            Student,
            AttendanceRecord.student_id == Student.id
        )

        .filter(
            AttendanceRecord.session_id == session_id
        )

        .all()

    )


    if not records:

        db.close()

        return None



    present = 0
    absent = 0


    students = []


    for record, student in records:


        if record.status == "Present":
            present += 1

        else:
            absent += 1



        students.append({

            "name": student.full_name,

            "student_number": student.student_number,

            "status": record.status

        })



    db.close()



    return {

        "session_id": session_id,

        "total_students": len(records),

        "present_count": present,

        "absent_count": absent,

        "students": students

    }