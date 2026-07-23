from attendance.attendance_service import (
    create_session,
    mark_remaining_absent
)

from database.db import SessionLocal

from database.models import AttendanceSession

from datetime import datetime



# =====================================
# ACTIVE SESSION STORAGE
# =====================================

active_session_id = None





# =====================================
# START NEW SESSION
# =====================================

def start_new_session(
    course_id,
    lecturer_id,
    user_id,
    period,
    session_date=None
):

    global active_session_id



    # Use current date if none selected

    if session_date is None:

        session_date = datetime.now()



    session_id = create_session(

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
# END SESSION
# =====================================

def end_session(session_id=None):

    global active_session_id



    if active_session_id is None:


        return (
            "⚠️ No active attendance session"
        )



    # Always close the running session

    current_session_id = active_session_id





    # Mark students not checked in as absent

    result = mark_remaining_absent(

        current_session_id

    )





    db = SessionLocal()



    session = db.query(

        AttendanceSession

    ).filter(

        AttendanceSession.id == current_session_id

    ).first()





    if session:


        session.closed = True

        db.commit()





    db.close()



    active_session_id = None





    return (

        result

        +

        f"\n🔴 Session {current_session_id} closed"

    )