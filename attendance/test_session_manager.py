from attendance.session_manager import (
    start_new_session,
    get_active_session,
    end_session
)



session = start_new_session(

    course_id=1,

    lecturer_id=1,

    user_id=1,

    period="Morning"

)


print(
    "Created session:",
    session
)



print(
    "Active session:",
    get_active_session()
)



print(
    end_session()
)