from database.db import SessionLocal
from database.models import AttendanceSession, AttendanceRecord, Student
from datetime import datetime


# =========================
# CREATE SESSION
# =========================
def create_session(course_id, period):
    db = SessionLocal()

    session = AttendanceSession(
        course_id=course_id,
        period=period,
        session_date=datetime.utcnow()
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()

    return session.id


# =========================
# MARK ATTENDANCE
# =========================
def mark_attendance(session_id, index_number):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.index_number == index_number
    ).first()

    if not student:
        db.close()
        return "Student not found"

    # ✅ COPY VALUE BEFORE CLOSING SESSION
    student_name = student.full_name

    record = AttendanceRecord(
        session_id=session_id,
        student_id=student.id,
        status="Present",
        timestamp=datetime.utcnow()
    )

    db.add(record)
    db.commit()
    db.close()

    return f"{student_name} marked present"

# =========================
# GET SESSION RECORDS
# =========================
def get_session_records(session_id):
    db = SessionLocal()

    records = db.query(AttendanceRecord).filter(
        AttendanceRecord.session_id == session_id
    ).all()

    db.close()
    return records