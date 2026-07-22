import sys

from PyQt5.QtWidgets import QApplication

from gui.attendance_window import AttendanceWindow



app = QApplication(sys.argv)



window = AttendanceWindow()



window.show()



# fake session

window.update_session(
    10
)



# fake class list

students = [

    {
        "name": "Kims",
        "student_number": "2300100666"
    },

    {
        "name": "John Smith",
        "student_number": "2300100667"
    },

    {
        "name": "Mary Jane",
        "student_number": "2300100668"
    }

]



window.load_students(
    students
)



# simulate voice recognition

window.mark_present(
    "2300100666",
    "10:30"
)


window.mark_present(
    "2300100667",
    "10:31"
)



app.exec_()