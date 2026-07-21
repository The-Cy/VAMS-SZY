from database.db import SessionLocal

from database.models import (
    Student,
    AttendanceRecord
)



def get_student_attendance_percentage(student_number):

    db = SessionLocal()


    student = db.query(
        Student
    ).filter(
        Student.student_number == student_number
    ).first()



    if not student:

        db.close()

        return None



    records = db.query(
        AttendanceRecord
    ).filter(
        AttendanceRecord.student_id == student.id
    ).all()



    total_classes = len(records)



    if total_classes == 0:

        percentage = 0

    else:

        present = len(
            [
                r for r in records
                if r.status == "Present"
            ]
        )

        percentage = (
            present / total_classes
        ) * 100



    db.close()



    return {

        "student_name": student.full_name,

        "student_number": student.student_number,

        "total_classes": total_classes,

        "attendance_percentage": round(
            percentage,
            2
        )

    }