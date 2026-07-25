"""PyQt5 administrator landing screen for the active VAMS-SZY flow."""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

from attendance.session_manager import get_active_session
from gui.session_window import SessionWindow
from gui.gui_manager import get_window
from gui.session_history import SessionHistoryWindow
from gui.report_window import ReportWindow


class AdminDashboard(QWidget):
    def __init__(self, user, on_session_started, on_logout):
        super().__init__()
        self.user = user
        self.on_session_started = on_session_started
        self.on_logout = on_logout
        self.session_window = None
        self.history_window = None
        self.report_window = None

        self.setWindowTitle("VAMS-SZY Admin Dashboard")
        self.resize(430, 420)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Welcome, {user.username} ({user.role})"))

        buttons = (
            ("Create Attendance Session", self.open_session_window),
            ("Active Attendance", self.open_active_attendance),
            ("Session History", self.open_session_history),
            ("Reports", self.open_reports),
            ("Logout", self.logout),
        )
        for text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            layout.addWidget(button)
        self.setLayout(layout)

    def open_session_window(self):
        if get_active_session():
            QMessageBox.information(
                self, "Active session", "Close the active attendance session first."
            )
            return
        self.session_window = SessionWindow(
            user_id=self.user.id, on_session_started=self.on_session_started
        )
        self.session_window.show()

    def open_active_attendance(self):
        if not get_active_session():
            QMessageBox.information(self, "Active attendance", "No active session exists.")
            return
        attendance = get_window()
        if attendance:
            attendance.show()
            attendance.raise_()
            attendance.activateWindow()

    def open_session_history(self):
        self.history_window = SessionHistoryWindow()
        self.history_window.show()

    def open_reports(self):
        self.report_window = ReportWindow()
        self.report_window.show()

    def logout(self):
        if get_active_session():
            QMessageBox.warning(
                self, "Active session", "Finish the active attendance session before logging out."
            )
            return
        self.on_logout()
