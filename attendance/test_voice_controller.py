from attendance.session_manager import start_new_session

from attendance.voice_controller import process_voice_command



# ===================================
# START ATTENDANCE SESSION
# ===================================

session = start_new_session(
    course_id=1,
    lecturer_id=1,
    user_id=1,
    period="Morning"
)


print(
    "Started session:",
    session
)



commands = [

    {
        "action":"attendance",
        "student_number":"2300100666",
        "name":"Kims",
        "status":"Present"
    },


    {
        "action":"attendance",
        "student_number":"2300100667",
        "name":"John",
        "status":"Present"
    },


    {
        "action":"finish"
    }

]



for command in commands:


    result = process_voice_command(
        command
    )


    print(result)