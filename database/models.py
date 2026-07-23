from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean
)

from datetime import datetime
from sqlalchemy.orm import relationship

from database.db import Base


# ======================================
# SYSTEM USERS (QA / ADMIN)
# ======================================
class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="QA"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ======================================
# STUDENT INFORMATION
# ======================================
class Student(Base):

    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True
    )

    student_number = Column(
        String,
        unique=True,
        nullable=False
    )

    index_number = Column(
        String,
        unique=True,
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )

    admission_year = Column(String)

    intake = Column(String)

    programme = Column(String)

    study_mode = Column(String)

    year_of_study = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    courses = relationship(
        "StudentCourse",
        back_populates="student"
    )


# ======================================
# LECTURERS
# ======================================
class Lecturer(Base):

    __tablename__ = "lecturers"

    id = Column(
        Integer,
        primary_key=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(String)

    department = Column(String)


# ======================================
# COURSE UNITS
# ======================================
class Course(Base):

    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    course_code = Column(
        String,
        unique=True,
        nullable=False
    )

    course_name = Column(
        String,
        nullable=False
    )

    credit_units = Column(Integer)

    semester = Column(String)

    students = relationship(
        "StudentCourse",
        back_populates="course"
    )


# ======================================
# STUDENT COURSE REGISTRATION
# MANY STUDENTS ↔ MANY COURSES
# ======================================
class StudentCourse(Base):

    __tablename__ = "student_courses"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id")
    )

    student = relationship(
        "Student",
        back_populates="courses"
    )

    course = relationship(
        "Course",
        back_populates="students"
    )


# ======================================
# DAILY ATTENDANCE SESSION
# Example:
# 07 July 2026
# Morning
# Database Systems
# ======================================
class AttendanceSession(Base):
    session_name = Column(
    String
)

    __tablename__ = "attendance_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id")
    )

    lecturer_id = Column(
        Integer,
        ForeignKey("lecturers.id")
    )

    started_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    session_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    period = Column(String)

    closed = Column(
        Boolean,
        default=False
    )

    records = relationship(
        "AttendanceRecord",
        back_populates="session"
    )


# ======================================
# INDIVIDUAL ATTENDANCE
# ======================================
class AttendanceRecord(Base):

    __tablename__ = "attendance_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("attendance_sessions.id")
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    status = Column(
        String,
        default="Present"
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    session = relationship(
        "AttendanceSession",
        back_populates="records"
    )

    student = relationship(
        "Student"
    )