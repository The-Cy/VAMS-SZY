from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QDateEdit,
    QMessageBox
)

from PyQt5.QtCore import QDate


from attendance.session_loader import (
    get_courses,
    get_lecturers
)

from attendance.session_manager import (
    start_new_session
)

from gui.gui_manager import (
    get_window
)



class SessionWindow(QWidget):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Create Attendance Session"
        )


        self.resize(
            450,
            450
        )


        layout = QVBoxLayout()



        # =================================
        # TITLE
        # =================================

        title = QLabel(
            "📅 Create Attendance Session"
        )


        layout.addWidget(
            title
        )




        # =================================
        # COURSE UNIT
        # =================================

        layout.addWidget(
            QLabel(
                "Course Unit"
            )
        )


        self.course_box = QComboBox()


        self.courses = get_courses()



        for course in self.courses:


            self.course_box.addItem(

                f"{course['code']} - {course['name']}",

                course["id"]

            )



        layout.addWidget(
            self.course_box
        )





        # =================================
        # LECTURER
        # =================================

        layout.addWidget(
            QLabel(
                "Lecturer"
            )
        )


        self.lecturer_box = QComboBox()


        self.lecturers = get_lecturers()



        for lecturer in self.lecturers:


            self.lecturer_box.addItem(

                lecturer["name"],

                lecturer["id"]

            )



        layout.addWidget(
            self.lecturer_box
        )





        # =================================
        # DATE
        # =================================

        layout.addWidget(
            QLabel(
                "Session Date"
            )
        )


        self.date_box = QDateEdit()


        self.date_box.setDate(

            QDate.currentDate()

        )


        self.date_box.setCalendarPopup(
            True
        )


        layout.addWidget(
            self.date_box
        )






        # =================================
        # PERIOD
        # =================================

        layout.addWidget(
            QLabel(
                "Period"
            )
        )


        self.period_box = QComboBox()


        self.period_box.addItems(

            [
                "Morning",
                "Afternoon",
                "Evening"
            ]

        )


        layout.addWidget(
            self.period_box
        )







        # =================================
        # START BUTTON
        # =================================

        self.start_button = QPushButton(

            "Start Attendance"

        )


        self.start_button.clicked.connect(

            self.create_session

        )


        layout.addWidget(
            self.start_button
        )



        self.setLayout(
            layout
        )






    # =====================================
    # CREATE SESSION
    # =====================================

    def create_session(self):


        # REAL DATABASE IDS

        course_id = self.course_box.currentData()


        lecturer_id = self.lecturer_box.currentData()



        if not course_id or not lecturer_id:


            QMessageBox.warning(

                self,

                "Missing Data",

                "Please select course and lecturer"

            )

            return





        user_id = 1




        session_date = (

            self.date_box.date()

            .toPyDate()

        )






        session_id = start_new_session(

            course_id=course_id,

            lecturer_id=lecturer_id,

            user_id=user_id,

            period=self.period_box.currentText(),

            session_date=session_date

        )





        QMessageBox.information(

            self,

            "Session Created",

            f"Attendance Session {session_id} Started"

        )





        attendance_window = get_window()



        if attendance_window:


            attendance_window.update_session(

                session_id

            )


            # next stage:
            # attendance_window.load_students(course_id)



        self.close()