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


        self.session_name = ""


        self.setWindowTitle(
            "Voice Attendance Management System"
        )


        self.resize(
            900,
            600
        )


        layout = QVBoxLayout()



        self.title = QLabel(
            "🎤 Voice Attendance System"
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            self.title
        )



        self.session_label = QLabel(
            "Session: Waiting"
        )

        layout.addWidget(
            self.session_label
        )



        self.summary_label = QLabel(
            "Present: 0 | Absent: 0"
        )

        layout.addWidget(
            self.summary_label
        )



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



    # =================================
    # SESSION DISPLAY
    # =================================

    def update_session(
        self,
        session_id,
        session_name=None
    ):


        if session_name:

            self.session_name = session_name


            self.session_label.setText(
                f"🟢 {session_name}"
            )

        else:

            self.session_label.setText(
                f"🟢 Active Session {session_id}"
            )



    # =================================
    # LOAD STUDENTS
    # =================================


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

            # The checkbox is a voice-controlled status indicator, not an
            # editable attendance input.
            checkbox.setFlags(Qt.ItemIsEnabled)

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
                self._read_only_item(student["name"])
            )


            self.table.setItem(
                row,
                2,
                self._read_only_item(student["student_number"])
            )


            self.table.setItem(
                row,
                3,
                self._read_only_item("Waiting")
            )


            self.table.setItem(
                row,
                4,
                self._read_only_item("-")
            )



    # =================================
    # VOICE PRESENT UPDATE
    # =================================


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
                    self._read_only_item("Present")
                )


                self.table.setItem(
                    row,
                    4,
                    self._read_only_item(timestamp)
                )


                break



        self.update_summary()



    # =================================
    # ABSENT ON CLOSE
    # =================================


    def mark_absent_remaining(self):


        for row in range(
            self.table.rowCount()
        ):


            checked = self.table.item(
                row,
                0
            ).checkState()



            if checked != Qt.Checked:


                self.table.item(
                    row,
                    0
                ).setCheckState(
                    Qt.Unchecked
                )


                self.table.setItem(
                    row,
                    3,
                    self._read_only_item("Absent")
                )

                self.table.setItem(
                    row,
                    4,
                    self._read_only_item("-")
                )


        self.update_summary()



    # =================================
    # SUMMARY
    # =================================


    def update_summary(self):


        present = 0
        absent = 0


        for row in range(
            self.table.rowCount()
        ):


            status = self.table.item(
                row,
                3
            ).text()



            if status == "Present":

                present += 1


            elif status == "Absent":

                absent += 1



        self.summary_label.setText(
            f"Present: {present} | Absent: {absent}"
        )


    @staticmethod
    def _read_only_item(text):

        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        return item



    # =================================
    # SESSION CLOSED
    # =================================


    def update_session_status(
        self,
        text
    ):

        self.session_label.setText(
            text
        )
