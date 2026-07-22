import sys

from PyQt5.QtWidgets import QApplication

from gui.attendance_window import AttendanceWindow

from speech.voice_thread import VoiceThread



app = QApplication(sys.argv)



window = AttendanceWindow()

window.show()



voice = VoiceThread()



def handle_command(command):


    print(
        "Command:",
        command
    )


    if command["action"] == "attendance":


        window.mark_present(

            command["student_number"],

            "NOW"

        )



    elif command["action"] == "finish":


        window.mark_absent_remaining()



voice.command_received.connect(
    handle_command
)



voice.start()



sys.exit(
    app.exec_()
)