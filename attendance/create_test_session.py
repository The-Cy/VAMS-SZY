from attendance.session_manager import start_new_session


session_id = start_new_session(

    course_id=1,

    lecturer_id=1,

    user_id=1,

    period="Morning"

)


print(
    "Created session:",
    session_id
)