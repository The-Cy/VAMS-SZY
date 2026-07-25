from datetime import datetime


from attendance.attendance_service import (
    mark_attendance
)


from attendance.session_manager import (
    get_active_session,
    end_session
)


from gui.gui_manager import (
    get_window
)





# =====================================
# PROCESS VOICE COMMAND
# =====================================

def process_voice_command(command):


    action = command.get(
        "action"
    )



    # =====================================
    # MARK ATTENDANCE
    # =====================================

    if action == "attendance":


        session_id = get_active_session()



        if not session_id:


            return (
                "❌ No active attendance session"
            )




        student_number = command.get(
            "student_number"
        )



        if not student_number:


            return (
                "❌ Student number missing"
            )




        status = command.get(
            "status",
            "Present"
        )




        result = mark_attendance(

            session_id=session_id,

            student_number=student_number,

            spoken_name=command.get(
                "name"
            ),

            status=status

        )




        # ==============================
        # UPDATE GUI LIVE
        # ==============================

        window = get_window()



        if window and result.startswith(
            "✅"
        ):


            window.mark_present(

                student_number,

                datetime.now().strftime(
                    "%H:%M:%S"
                )

            )



        return result







    # =====================================
    # CLOSE SESSION
    # =====================================

    if action == "finish":



        session_id = get_active_session()



        if not session_id:


            return (

                "❌ No active session"

            )




        result = end_session(

            session_id

        )




        window = get_window()



        if window:


            window.mark_absent_remaining()



            if hasattr(
                window,
                "update_session_status"
            ):


                window.update_session_status(

                    "🔴 Session Closed"

                )



        return result






    # =====================================
    # UNKNOWN COMMAND
    # =====================================

    return (

        "❌ Unknown command"

    )