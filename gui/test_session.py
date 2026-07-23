import sys

from PyQt5.QtWidgets import QApplication

from gui.session_window import SessionWindow



app = QApplication(sys.argv)


window = SessionWindow()

window.show()


sys.exit(
    app.exec_()
)