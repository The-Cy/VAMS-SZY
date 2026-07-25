"""Read-only attendance summary and CSV export screen."""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

from attendance.session_summary import get_session_summary
from attendance.export_report import export_session_csv
from database.db import SessionLocal
from database.models import AttendanceSession


class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Reports")
        self.resize(720, 500)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Attendance Summary and CSV Export"))
        controls = QHBoxLayout()
        self.session_box = QComboBox()
        controls.addWidget(self.session_box)
        refresh = QPushButton("Refresh Sessions")
        refresh.clicked.connect(self.load_sessions)
        controls.addWidget(refresh)
        generate = QPushButton("Generate Report")
        generate.clicked.connect(self.generate_report)
        controls.addWidget(generate)
        layout.addLayout(controls)
        self.summary_label = QLabel("Select a session and generate its report.")
        layout.addWidget(self.summary_label)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Student Number", "Student Name", "Status"])
        layout.addWidget(self.table)
        export = QPushButton("Export Current Session to CSV")
        export.clicked.connect(self.export_csv)
        layout.addWidget(export)
        self.setLayout(layout)
        self.load_sessions()

    def load_sessions(self):
        current_id = self.session_box.currentData()
        self.session_box.clear()
        db = SessionLocal()
        try:
            sessions = db.query(AttendanceSession).order_by(
                AttendanceSession.session_date.desc(), AttendanceSession.id.desc()
            ).all()
            for session in sessions:
                status = "Closed" if session.closed else "Active"
                self.session_box.addItem(
                    f"{session.session_name} ({status})", session.id
                )
        finally:
            db.close()
        index = self.session_box.findData(current_id)
        if index >= 0:
            self.session_box.setCurrentIndex(index)

    @staticmethod
    def _item(text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        return item

    def generate_report(self):
        session_id = self.session_box.currentData()
        if session_id is None:
            self.summary_label.setText("No sessions are available.")
            return
        summary = get_session_summary(session_id)
        if summary is None:
            self.summary_label.setText("No report data exists for this session.")
            self.table.setRowCount(0)
            return
        self.summary_label.setText(
            f"Total: {summary['total_students']} | Present: {summary['present_count']} | "
            f"Absent: {summary['absent_count']}"
        )
        self.table.setRowCount(0)
        for student in summary["present"] + summary["absent"]:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = (student["student_number"], student["name"], student["status"])
            for column, value in enumerate(values):
                self.table.setItem(row, column, self._item(value))

    def export_csv(self):
        session_id = self.session_box.currentData()
        if session_id is None:
            QMessageBox.warning(self, "Export", "Select a session first.")
            return
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save attendance report", "attendance_report.csv", "CSV files (*.csv)"
        )
        if not filename:
            return
        result = export_session_csv(session_id, filename)
        QMessageBox.information(self, "Export report", result)
