from rapidfuzz import fuzz

from database.db import SessionLocal

from database.models import (
    Student,
    AttendanceRecord,
    AttendanceSession,
    StudentCourse
)

from datetime import datetime



# =====================================================
# CREATE ATTENDANCE SESSION
# =====================================================
# Creates:
#
# Course Unit
# Lecturer
# QA User
# Date
# Period
#
# Example:
# Database Systems
# Mr Jeff
# QA1
# Morning
# 21/07/2026
# =====================================================

from database.db import SessionLocal
from database.models import AttendanceSession



def create_session(
    session_name,
    course_id,
    lecturer_id,
    user_id,
    period,
    session_date
):


    db = SessionLocal()


    session = AttendanceSession(

        session_name=session_name,

        course_id=course_id,

        lecturer_id=lecturer_id,

        started_by=user_id,

        period=period,

        session_date=session_date

    )


    db.add(session)

    db.commit()

    db.refresh(session)


    db.close()


    return session.id

# =====================================================
# MARK ATTENDANCE
# =====================================================
#
# Voice example:
#
# "Kims 2300100666 present"
#
# Main identifier:
# student_number
#
# Name:
# optional verification
#
# =====================================================


def mark_attendance(
    session_id,
    student_number,
    spoken_name=None,
    status="Present"
):

    db = SessionLocal()



    # -----------------------------------------
    # Check session exists
    # -----------------------------------------

    session = db.query(
        AttendanceSession
    ).filter(

        AttendanceSession.id == session_id

    ).first()



    if not session:


        db.close()

        return "❌ Attendance session not found"





    # -----------------------------------------
    # Find student registered for this course
    # -----------------------------------------

    student = (

        db.query(Student)

        .join(

            StudentCourse,

            Student.id == StudentCourse.student_id

        )

        .filter(

            Student.student_number == student_number,

            StudentCourse.course_id == session.course_id

        )

        .first()

    )



    if not student:


        db.close()


        return (
            "❌ Student not found "
            "or not registered for this course"
        )





    # -----------------------------------------
    # Optional name verification
    # -----------------------------------------

    # ---------------------------------
# Optional name verification
# Student number remains primary key
# ---------------------------------

    if spoken_name:

        score = fuzz.partial_ratio(
            spoken_name.lower(),
            student.full_name.lower()
        )

        if score < 40:

            print(
                f"⚠️ Name mismatch ignored. "
                f"Using student number."
            )







    # -----------------------------------------
    # Prevent duplicate attendance
    # -----------------------------------------

    existing = db.query(
        AttendanceRecord
    ).filter(

        AttendanceRecord.session_id == session_id,

        AttendanceRecord.student_id == student.id

    ).first()



    if existing:


        db.close()


        return (
            f"⚠️ Already marked: "
            f"{student.full_name}"
        )







    # -----------------------------------------
    # Create attendance record
    # -----------------------------------------

    record = AttendanceRecord(

        session_id=session_id,

        student_id=student.id,

        status=status,

        timestamp=datetime.utcnow()

    )


    db.add(record)

    db.commit()



    name = student.full_name



    db.close()



    return (

        f"✅ {name} "

        f"({student_number}) "

        f"marked {status}"

    )







# =====================================================
# AUTO MARK REMAINING STUDENTS ABSENT
# =====================================================
#
# Called when QA says:
#
# "finish attendance"
#
# Any student not recorded becomes absent.
#
# =====================================================


def mark_remaining_absent(session_id):


    db = SessionLocal()



    # -----------------------------------------
    # Get session
    # -----------------------------------------

    session = db.query(
        AttendanceSession
    ).filter(

        AttendanceSession.id == session_id

    ).first()



    if not session:


        db.close()


        return "❌ Session not found"







    # -----------------------------------------
    # Get all students registered
    # for selected course
    # -----------------------------------------

    students = (

        db.query(Student)

        .join(

            StudentCourse,

            Student.id == StudentCourse.student_id

        )

        .filter(

            StudentCourse.course_id == session.course_id

        )

        .all()

    )







    added = 0





    # -----------------------------------------
    # Add absent records
    # for students not mentioned
    # -----------------------------------------

    for student in students:



        existing = db.query(
            AttendanceRecord
        ).filter(

            AttendanceRecord.session_id == session_id,

            AttendanceRecord.student_id == student.id

        ).first()



        if not existing:



            record = AttendanceRecord(

                session_id=session_id,

                student_id=student.id,

                status="Absent",

                timestamp=datetime.utcnow()

            )


            db.add(record)


            added += 1







    # -----------------------------------------
    # Close session
    # -----------------------------------------

    session.closed = True



    db.commit()



    db.close()



    return (

        f"✅ Attendance completed. "

        f"{added} students marked absent."

    )