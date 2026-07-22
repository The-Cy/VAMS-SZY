from gui.attendance_window import AttendanceWindow


window = None


def start_gui(app):

    global window

    window = AttendanceWindow()

    window.show()



def get_window():

    return window