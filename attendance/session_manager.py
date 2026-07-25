from attendance.attendance_service import (
    create_session,
    mark_remaining_absent
)


from database.db import SessionLocal


from database.models import AttendanceSession, Course
from datetime import datetime, time



active_session_id = None




# =====================================
# START SESSION
# =====================================

def start_new_session(
    course_id,
    lecturer_id,
    user_id,
    period,
    session_date=None,
    session_name=None
):


    global active_session_id



    if session_date is None:
        session_date = datetime.now()

    # QDateEdit provides a ``date``.  Store a real datetime because the model
    # is DateTime and other database engines are stricter than SQLite.
    if not isinstance(session_date, datetime):
        session_date = datetime.combine(session_date, time.min)

    if not session_name:
        db = SessionLocal()
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            course_name = course.course_name if course else "Attendance"
        finally:
            db.close()
        session_name = (
            f"{course_name} - {period} Session - "
            f"{session_date.date().isoformat()}"
        )

    session_id = create_session(

        session_name=session_name,

        course_id=course_id,

        lecturer_id=lecturer_id,

        user_id=user_id,

        period=period,

        session_date=session_date

    )



    active_session_id = session_id


    return session_id





# =====================================
# GET ACTIVE SESSION
# =====================================

def get_active_session():

    return active_session_id





# =====================================
# CLOSE SESSION
# =====================================

def end_session(session_id=None):


    global active_session_id



    if not active_session_id:

        return "⚠️ No active session"



    session_id = active_session_id



    result = mark_remaining_absent(
        session_id
    )



    db = SessionLocal()



    session = db.query(
        AttendanceSession
    ).filter(
        AttendanceSession.id == session_id
    ).first()



    if session:

        session.closed = True

        # Keep ordinary data before commit/close. SQLAlchemy expires ORM
        # objects on commit, so accessing ``session.session_name`` after
        # ``db.close()`` raises DetachedInstanceError.
        closed_session_name = session.session_name

        db.commit()

    else:

        closed_session_name = "Unknown session"



    db.close()



    active_session_id = None



    return (

        result +

        f"\n🔴 Session closed: {closed_session_name}"

    )
