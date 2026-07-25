"""PyQt5 login window used by the active VAMS-SZY application flow."""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

from database.db import SessionLocal
from database.models import User


class LoginWindow(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.setWindowTitle("VAMS-SZY Login")
        self.resize(380, 240)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Voice Attendance Management System"))
        layout.addWidget(QLabel("Username"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Login", "Enter both username and password.")
            return

        db = SessionLocal()
        try:
            user = db.query(User).filter(
                User.username == username, User.password == password
            ).first()
            if user is None:
                QMessageBox.warning(self, "Login failed", "Invalid username or password.")
                return
            db.expunge(user)
        finally:
            db.close()

        self.password_input.clear()
        self.on_login(user)

    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
