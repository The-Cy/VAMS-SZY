from rapidfuzz import fuzz
from database.db import SessionLocal
from database.models import (
    Student,
    AttendanceRecord,
    AttendanceSession
)
from datetime import datetime


# =========================
# CREATE SESSION
# =========================
def create_session(course_id=1, period="Morning"):
    db = SessionLocal()

    session = AttendanceSession(
        course_id=course_id,
        period=period,
        session_date=datetime.utcnow()
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    session_id = session.id
    db.close()

    return session_id


# =========================
# MARK ATTENDANCE (FINAL VERSION)
# =========================
def mark_attendance(
    session_id,
    index_number,
    spoken_name=None,
    status="Present"
):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.index_number == index_number
    ).first()

    if not student:
        db.close()
        return "❌ Student not found"

    # =========================
    # FUZZY NAME CHECK
    # =========================
    if spoken_name:
        score = fuzz.partial_ratio(
            spoken_name.lower(),
            student.full_name.lower()
        )

        if score < 60:
            db.close()
            return (
                f"⚠️ Name unclear (confidence {score/100:.2f}). "
                f"DB says: {student.full_name}"
            )

    # =========================
    # DUPLICATE CHECK
    # =========================
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.session_id == session_id,
        AttendanceRecord.student_id == student.id
    ).first()

    if existing:
        db.close()
        return f"⚠️ Already marked: {student.full_name}"

    # =========================
    # CREATE RECORD
    # =========================
    record = AttendanceRecord(
        session_id=session_id,
        student_id=student.id,
        status=status,
        timestamp=datetime.utcnow()
    )

    db.add(record)
    db.commit()

    name = student.full_name
    db.close()

    return f"✅ {name} ({index_number}) marked {status}"