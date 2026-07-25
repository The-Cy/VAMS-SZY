"""Main VAMS-SZY application launcher.

The microphone is deliberately started only after a user logs in and creates
an attendance session.
"""

import sys

from PyQt5.QtWidgets import QApplication

from attendance.voice_controller import process_voice_command
from database.bootstrap import initialize_database
from database.seed import seed_database
from gui.admin_dashboard import AdminDashboard
from gui.app_state import clear_active_user, set_active_user
from gui.attendance_window import AttendanceWindow
from gui.gui_manager import set_window
from gui.login_window import LoginWindow
from speech.voice_thread import VoiceThread


def start_application():
    initialize_database()
    seed_database()

    app = QApplication(sys.argv)
    attendance_window = AttendanceWindow()
    set_window(attendance_window)
    state = {"voice_thread": None, "dashboard": None}

    def handle_command(command):
        print("Command:", command)
        try:
            print(process_voice_command(command))
        except Exception as error:
            print("Voice processing error:", error)

    def start_voice_for_session(_session_id):
        voice_thread = state["voice_thread"]
        if voice_thread and voice_thread.isRunning():
            return
        voice_thread = VoiceThread()
        voice_thread.command_received.connect(handle_command)
        voice_thread.start()
        state["voice_thread"] = voice_thread

    def logout():
        dashboard = state["dashboard"]
        if dashboard:
            dashboard.close()
        state["dashboard"] = None
        clear_active_user()
        login_window.clear_form()
        login_window.show()

    def open_dashboard(user):
        set_active_user(user)
        login_window.hide()
        dashboard = AdminDashboard(user, start_voice_for_session, logout)
        state["dashboard"] = dashboard
        dashboard.show()

    login_window = LoginWindow(open_dashboard)
    login_window.show()

    def close_application():
        voice_thread = state["voice_thread"]
        if voice_thread and voice_thread.isRunning():
            voice_thread.stop()
            voice_thread.wait()

    app.aboutToQuit.connect(close_application)
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Voice Attendance System Started")
    start_application()
