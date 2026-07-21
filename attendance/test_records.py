from database.db import SessionLocal

from database.models import (
    AttendanceRecord,
    Student
)


SESSION_ID = 6


db = SessionLocal()


records = db.query(
    AttendanceRecord
).filter(
    AttendanceRecord.session_id == SESSION_ID
).all()



print("\n===== SESSION", SESSION_ID, "ATTENDANCE =====")


for record in records:


    student = db.query(
        Student
    ).filter(
        Student.id == record.student_id
    ).first()



    print(
        student.full_name,
        student.student_number,
        record.status
    )


db.close()