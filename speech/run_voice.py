import sys


from PyQt5.QtWidgets import QApplication


from gui.attendance_window import AttendanceWindow


from gui.gui_manager import set_window


from speech.voice_thread import VoiceThread


from attendance.voice_controller import process_voice_command





def start_application():


    app = QApplication(
        sys.argv
    )



    # ==========================
    # CREATE WINDOW
    # ==========================

    window = AttendanceWindow()

    window.show()



    # REGISTER GUI GLOBALLY

    set_window(
        window
    )




    # ==========================
    # VOICE THREAD
    # ==========================

    voice_thread = VoiceThread()



    def handle_command(command):


        print(
            "Command:",
            command
        )


        try:


            result = process_voice_command(
                command
            )


            print(
                result
            )


        except Exception as e:


            print(
                "GUI ERROR:",
                e
            )




    voice_thread.command_received.connect(
        handle_command
    )



    voice_thread.start()




    def close_application():


        voice_thread.stop()

        voice_thread.wait()



    app.aboutToQuit.connect(
        close_application
    )



    sys.exit(
        app.exec_()
    )





if __name__ == "__main__":


    print(
        "🎤 Voice Attendance System Started"
    )


    start_application()