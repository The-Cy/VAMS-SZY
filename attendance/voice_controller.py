from datetime import datetime


from attendance.student_loader import (
    get_course_students
)


from attendance.attendance_service import (
    mark_attendance
)


from attendance.session_manager import (
    get_active_session,
    start_new_session,
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
    # START ATTENDANCE
    # =====================================

    if action == "start":


        # TEMPORARY
        # later this comes from SessionWindow

        course_id = 1



        session_id = start_new_session(

            course_id=course_id,

            lecturer_id=1,

            user_id=1,

            period="Morning"

        )



        print(
            "SESSION CREATED:",
            session_id
        )



        window = get_window()



        if window:


            print(
                "GUI FOUND"
            )



            window.update_session(

                session_id

            )



            students = get_course_students(

                course_id

            )



            print(
                "STUDENTS:",
                students
            )



            window.load_students(

                students

            )



        else:


            print(
                "GUI WINDOW NOT FOUND"
            )



        return (

            f"🟢 Attendance started "
            f"Session {session_id}"

        )





    # =====================================
    # MARK PRESENT
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
    # FINISH SESSION
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
    # UNKNOWN
    # =====================================

    return (

        "❌ Unknown command"

    )