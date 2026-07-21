from attendance.attendance_service import mark_attendance
from attendance.session_manager import (
    get_active_session,
    end_session
)



def process_voice_command(command):


    action = command.get("action")



    # =================================
    # ATTENDANCE COMMAND
    # =================================

    if action == "attendance":


        session_id = get_active_session()


        if not session_id:

            return "❌ No active attendance session"



        result = mark_attendance(

            session_id=session_id,

            student_number=command["student_number"],

            spoken_name=command.get("name"),

            status=command.get(
                "status",
                "Present"
            )

        )


        return result



    # =================================
    # FINISH COMMAND
    # =================================

    elif action == "finish":


        session_id = get_active_session()


        if not session_id:

            return "❌ No active attendance session"



        result = end_session(
            session_id
        )


        return result



    return "❌ Unknown command"