from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)

from PyQt5.QtCore import Qt



class AttendanceWindow(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Voice Attendance Management System"
        )


        self.resize(
            900,
            600
        )


        layout = QVBoxLayout()



        # TITLE

        self.title = QLabel(
            "🎤 Voice Attendance System"
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            self.title
        )



        # SESSION

        self.session_label = QLabel(
            "Session: Waiting"
        )

        layout.addWidget(
            self.session_label
        )



        # SUMMARY

        self.summary_label = QLabel(
            "Present: 0 | Absent: 0"
        )

        layout.addWidget(
            self.summary_label
        )



        # TABLE

        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Present",
                "Name",
                "Student Number",
                "Status",
                "Time"
            ]
        )


        layout.addWidget(
            self.table
        )



        # CLOSE

        self.close_button = QPushButton(
            "Close Window"
        )


        self.close_button.clicked.connect(
            self.close
        )


        layout.addWidget(
            self.close_button
        )


        self.setLayout(
            layout
        )



    # ===============================
    # SESSION
    # ===============================

    def update_session(
        self,
        session_id
    ):

        self.session_label.setText(
            f"🟢 Active Session: {session_id}"
        )



    # ===============================
    # LOAD CLASS LIST
    # ===============================

    def load_students(
        self,
        students
    ):


        self.table.setRowCount(
            0
        )


        for student in students:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            checkbox = QTableWidgetItem()

            checkbox.setCheckState(
                Qt.Unchecked
            )


            self.table.setItem(
                row,
                0,
                checkbox
            )


            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    student["name"]
                )
            )


            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    student["student_number"]
                )
            )


            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    "Waiting"
                )
            )


            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    "-"
                )
            )



    # ===============================
    # MARK PRESENT
    # ===============================

    def mark_present(
        self,
        student_number,
        timestamp
    ):


        for row in range(
            self.table.rowCount()
        ):


            number = self.table.item(
                row,
                2
            ).text()



            if number == student_number:


                self.table.item(
                    row,
                    0
                ).setCheckState(
                    Qt.Checked
                )


                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        "Present"
                    )
                )


                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        timestamp
                    )
                )


                break



    # ===============================
    # MARK ABSENT AFTER FINISH
    # ===============================

    def mark_absent_remaining(self):


        for row in range(
            self.table.rowCount()
        ):


            checked = self.table.item(
                row,
                0
            ).checkState()



            if checked != Qt.Checked:


                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        "Absent"
                    )
                )


                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        "-"
                    )
                )