from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from database.db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    index_number = Column(String, unique=True, nullable=False)
    programme = Column(String)
    year_of_study = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)



class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, nullable=False)
    course_name = Column(String, nullable=False)


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    session_date = Column(DateTime, default=datetime.utcnow)
    period = Column(String)  # Morning / Afternoon / Evening


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(String, default="Present")  # Present / Absent
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="QA")  # Admin, QA, Lecturer