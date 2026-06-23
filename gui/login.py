import sys
from gui.dashboard import Dashboard
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

from database.db import SessionLocal
from database.models import User


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Attendance System - Login")
        self.setGeometry(300, 200, 400, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Login to System")
        layout.addWidget(self.label)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.button = QPushButton("Login")
        self.button.clicked.connect(self.check_login)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def check_login(self):
        user_input = self.username.text()
        pwd_input = self.password.text()

        db = SessionLocal()

        user = db.query(User).filter(
            User.username == user_input,
            User.password == pwd_input
        ).first()

        db.close()

        if user:
            self.dashboard = Dashboard(user.role)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid Credentials")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())