import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout, QMessageBox
)

from attendance.attendance_service import create_session, mark_attendance
from gui.student_window import StudentWindow


class Dashboard(QWidget):
    def __init__(self, user_role):
        super().__init__()

        self.user_role = user_role
        self.session_id = None

        self.setWindowTitle("Voice Attendance System - Dashboard")
        self.setGeometry(300, 200, 500, 300)

        layout = QVBoxLayout()

        self.label = QLabel(f"Welcome ({self.user_role})")
        layout.addWidget(self.label)

        # SESSION
        self.start_btn = QPushButton("Start Attendance 🎤")
        self.start_btn.clicked.connect(self.start_session)
        layout.addWidget(self.start_btn)

        self.test_btn = QPushButton("Mark Test Student (23001)")
        self.test_btn.clicked.connect(self.mark_test)
        layout.addWidget(self.test_btn)

        # STUDENTS MODULE
        self.students_window = StudentWindow()
        self.students_btn = QPushButton("Manage Students")
        self.students_btn.clicked.connect(self.students_window.show)
        layout.addWidget(self.students_btn)

        # PLACEHOLDERS
        layout.addWidget(QPushButton("View Sessions"))
        layout.addWidget(QPushButton("Reports"))

        self.setLayout(layout)

    # -------------------------
    def start_session(self):
        try:
            self.session_id = create_session(course_id=1, period="Morning")
            QMessageBox.information(self, "Session", f"Session ID: {self.session_id}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # -------------------------
    def mark_test(self):
        if not self.session_id:
            QMessageBox.warning(self, "Warning", "Start session first")
            return

        try:
            result = mark_attendance(self.session_id, "23001")
            QMessageBox.information(self, "Attendance", result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard("Admin")
    window.show()
    sys.exit(app.exec())