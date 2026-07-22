from PyQt5.QtCore import QThread, pyqtSignal

from speech.recognizer import listen
from speech.parser import parse_attendance_command



class VoiceThread(QThread):


    command_received = pyqtSignal(dict)


    def __init__(self):

        super().__init__()

        self.running = True



    def run(self):


        print("🎤 Voice thread started")


        while self.running:


            text = listen()


            print(
                "Recognized:",
                text
            )


            command = parse_attendance_command(
                text
            )


            self.command_received.emit(
                command
            )



    def stop(self):

        self.running = False