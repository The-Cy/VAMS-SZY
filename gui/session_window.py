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

from attendance.student_loader import (
    get_course_students
)

from gui.gui_manager import (
    get_window
)





class SessionWindow(QWidget):


    def __init__(self, user_id=1, on_session_started=None):

        super().__init__()

        self.user_id = user_id
        self.on_session_started = on_session_started


        self.setWindowTitle(
            "Create Attendance Session"
        )


        self.resize(
            450,
            450
        )


        layout = QVBoxLayout()



        layout.addWidget(
            QLabel(
                "📅 Create Attendance Session"
            )
        )



        # COURSE

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



        # LECTURER

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



        # DATE


        layout.addWidget(
            QLabel(
                "Date"
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




        # PERIOD


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




        # BUTTON


        button = QPushButton(
            "Start Attendance"
        )


        button.clicked.connect(
            self.create_session
        )


        layout.addWidget(
            button
        )



        self.setLayout(
            layout
        )





    def create_session(self):


        if not self.courses or not self.lecturers:
            QMessageBox.warning(
                self,
                "Missing setup data",
                "No courses or lecturers are available. Run the database seed first."
            )
            return


        course_id = self.course_box.currentData()

        lecturer_id = self.lecturer_box.currentData()



        course = self.courses[
            self.course_box.currentIndex()
        ]



        date = self.date_box.date().toPyDate()



        period = self.period_box.currentText()



        session_name = (

            f"{course['name']} - "

            f"{period} Session - "

            f"{date}"

        )



        session_id = start_new_session(

    course_id=course_id,

    lecturer_id=lecturer_id,

    user_id=self.user_id,

    period=period,

    session_date=date,

    session_name=session_name

)

        attendance = get_window()



        if attendance:


            attendance.update_session(
                session_id,
                session_name
            )


            students = get_course_students(
                course_id
            )


            attendance.load_students(
                students
            )


            attendance.show()


        if self.on_session_started:

            self.on_session_started(session_id)



        QMessageBox.information(

            self,

            "Started",

            session_name

        )


        self.close()
