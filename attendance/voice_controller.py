from attendance.attendance_service import (
    mark_attendance
)

from attendance.session_manager import (
    get_active_session,
    start_new_session,
    end_session
)


from gui.gui_manager import get_window



# =====================================
# PROCESS VOICE COMMAND
# =====================================

def process_voice_command(command):


    action = command.get(
        "action"
    )



    # =========================
    # START
    # =========================

    if action == "start":


        session_id = start_new_session(
            course_id=1,
            lecturer_id=1,
            user_id=1,
            period="Morning"
        )


        window = get_window()


        if window:

            window.update_session(
                session_id
            )


        return (
            f"🟢 Attendance started "
            f"Session {session_id}"
        )



    # =========================
    # ATTENDANCE
    # =========================

    if action == "attendance":


        session_id = get_active_session()



        if not session_id:

            return (
                "❌ No active attendance session"
            )



        result = mark_attendance(

            session_id=session_id,

            student_number=
            command["student_number"],

            spoken_name=
            command.get("name"),

            status=
            command.get("status","Present")

        )



        # update GUI

        window = get_window()



        if window and result.startswith("✅"):


            window.add_record(

                command.get(
                    "name",
                    "Unknown"
                ),

                command[
                    "student_number"
                ],

                command[
                    "status"
                ]

            )



        return result




    # =========================
    # FINISH
    # =========================

    if action == "finish":


        session_id = get_active_session()


        if not session_id:

            return (
                "❌ No active session"
            )



        result = end_session(
            session_id
        )



        return result



    return "❌ Unknown command"