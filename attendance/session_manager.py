from attendance.attendance_service import (
    create_session,
    mark_remaining_absent
)

from database.db import SessionLocal

from database.models import AttendanceSession

from datetime import datetime


# Stores currently running session
active_session_id = None



# =====================================
# START NEW SESSION
# =====================================

def start_new_session(
    course_id,
    lecturer_id,
    user_id,
    period
):

    global active_session_id


    session_id = create_session(
        course_id=course_id,
        lecturer_id=lecturer_id,
        user_id=user_id,
        period=period,
        session_date=datetime.now()
    )


    active_session_id = session_id


    return session_id





# =====================================
# GET CURRENT SESSION
# =====================================

def get_active_session():

    return active_session_id





# =====================================
# END SESSION
# =====================================

def end_session(session_id):
    global active_session_id


    if active_session_id is None:

        return "⚠️ No active attendance session"



    session_id = active_session_id



    # Mark students who never responded absent

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

        db.commit()



    db.close()



    active_session_id = None



    return (
        result
        +
        f"\n🔴 Session {session_id} closed"
    )