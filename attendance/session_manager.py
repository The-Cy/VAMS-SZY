active_session = None


def start_new_session(course_id=1, period="Morning"):
    global active_session

    from attendance.attendance_service import create_session

    active_session = create_session(course_id, period)

    return active_session


def get_active_session():
    return active_session


def end_session():
    global active_session

    ended = active_session
    active_session = None

    return ended