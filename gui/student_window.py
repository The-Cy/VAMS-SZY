from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QMessageBox, QListWidget
)

from attendance.student_service import (
    add_student,
    get_all_students,
    delete_student
)


class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setGeometry(300, 200, 500, 400)

        layout = QVBoxLayout()

        # INPUTS
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        layout.addWidget(self.name_input)

        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("Index Number")
        layout.addWidget(self.index_input)

        self.programme_input = QLineEdit()
        self.programme_input.setPlaceholderText("Programme")
        layout.addWidget(self.programme_input)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year of Study")
        layout.addWidget(self.year_input)

        # BUTTONS
        self.add_btn = QPushButton("Add Student")
        self.add_btn.clicked.connect(self.add_student)
        layout.addWidget(self.add_btn)

        self.load_btn = QPushButton("Load Students")
        self.load_btn.clicked.connect(self.load_students)
        layout.addWidget(self.load_btn)

        self.delete_btn = QPushButton("Delete Selected Student")
        self.delete_btn.clicked.connect(self.delete_student)
        layout.addWidget(self.delete_btn)

        # LIST
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    # -------------------------
    # ADD STUDENT
    # -------------------------
    def add_student(self):
        try:
            add_student(
                self.name_input.text(),
                self.index_input.text(),
                self.programme_input.text(),
                self.year_input.text()
            )

            QMessageBox.information(self, "Success", "Student added successfully")
            self.clear_inputs()
            self.load_students()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # -------------------------
    # LOAD STUDENTS
    # -------------------------
    def load_students(self):
        self.list_widget.clear()

        students = get_all_students()

        for s in students:
            self.list_widget.addItem(
                f"{s.full_name} | {s.index_number} | {s.programme} | {s.year_of_study}"
            )

    # -------------------------
    # DELETE STUDENT
    # -------------------------
    def delete_student(self):
        selected = self.list_widget.currentItem()

        if not selected:
            QMessageBox.warning(self, "Warning", "Select a student first")
            return

        index_number = selected.text().split("|")[1].strip()

        try:
            delete_student(index_number)
            QMessageBox.information(self, "Deleted", "Student removed")
            self.load_students()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # -------------------------
    # CLEAR INPUTS
    # -------------------------
    def clear_inputs(self):
        self.name_input.clear()
        self.index_input.clear()
        self.programme_input.clear()
        self.year_input.clear()