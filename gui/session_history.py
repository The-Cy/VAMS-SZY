"""Searchable read-only session history for attendance administrators."""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

from database.db import SessionLocal
from database.models import AttendanceSession, Course, Lecturer
from gui.session_details import SessionDetailsWindow


class SessionHistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.details_window = None
        self.setWindowTitle("Attendance Session History")
        self.resize(900, 500)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Session History"))
        controls = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by session name, course, or lecturer")
        self.search_box.textChanged.connect(self.load_sessions)
        controls.addWidget(self.search_box)
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.load_sessions)
        controls.addWidget(refresh)
        layout.addLayout(controls)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Session Name", "Course", "Lecturer", "Date", "Period", "Status"]
        )
        self.table.cellDoubleClicked.connect(self.open_selected_session)
        layout.addWidget(self.table)
        details = QPushButton("Open Selected Session Details")
        details.clicked.connect(self.open_selected_session)
        layout.addWidget(details)
        self.setLayout(layout)
        self.load_sessions()

    @staticmethod
    def _item(text, session_id=None):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        if session_id is not None:
            item.setData(Qt.UserRole, session_id)
        return item

    def load_sessions(self):
        search = self.search_box.text().strip().lower()
        db = SessionLocal()
        try:
            rows = (
                db.query(AttendanceSession, Course, Lecturer)
                .join(Course, AttendanceSession.course_id == Course.id)
                .join(Lecturer, AttendanceSession.lecturer_id == Lecturer.id)
                .order_by(AttendanceSession.session_date.desc(), AttendanceSession.id.desc())
                .all()
            )
            self.table.setRowCount(0)
            for session, course, lecturer in rows:
                searchable = " ".join((session.session_name, course.course_name, lecturer.full_name)).lower()
                if search and search not in searchable:
                    continue
                row = self.table.rowCount()
                self.table.insertRow(row)
                values = (
                    session.session_name,
                    f"{course.course_code} - {course.course_name}",
                    lecturer.full_name,
                    session.session_date.strftime("%d/%m/%Y") if session.session_date else "-",
                    session.period or "-",
                    "Closed" if session.closed else "Active",
                )
                for column, value in enumerate(values):
                    self.table.setItem(
                        row, column, self._item(value, session.id if column == 0 else None)
                    )
        finally:
            db.close()

    def open_selected_session(self, *_):
        row = self.table.currentRow()
        if row < 0:
            return
        session_id = self.table.item(row, 0).data(Qt.UserRole)
        self.details_window = SessionDetailsWindow(session_id)
        self.details_window.show()
