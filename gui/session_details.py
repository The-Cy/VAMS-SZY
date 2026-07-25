"""Read-only attendance records for one completed or active session."""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

from database.db import SessionLocal
from database.models import AttendanceSession, AttendanceRecord, Student


class SessionDetailsWindow(QWidget):
    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id
        self.setWindowTitle("Session Attendance Details")
        self.resize(720, 460)
        layout = QVBoxLayout()
        self.title = QLabel()
        layout.addWidget(self.title)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Student Name", "Student Number", "Status", "Time"])
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_records()

    @staticmethod
    def _item(text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        return item

    def load_records(self):
        db = SessionLocal()
        try:
            session = db.query(AttendanceSession).filter_by(id=self.session_id).first()
            if session is None:
                self.title.setText("Session not found")
                return
            self.title.setText(session.session_name)
            records = (
                db.query(AttendanceRecord, Student)
                .join(Student, AttendanceRecord.student_id == Student.id)
                .filter(AttendanceRecord.session_id == self.session_id)
                .order_by(Student.full_name)
                .all()
            )
            self.table.setRowCount(0)
            for record, student in records:
                row = self.table.rowCount()
                self.table.insertRow(row)
                values = (
                    student.full_name,
                    student.student_number,
                    record.status,
                    record.timestamp.strftime("%H:%M:%S") if record.timestamp else "-",
                )
                for column, value in enumerate(values):
                    self.table.setItem(row, column, self._item(value))
        finally:
            db.close()
