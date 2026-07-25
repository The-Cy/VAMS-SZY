"""Idempotent demo data for VAMS-SZY development and demonstrations."""

from database.bootstrap import initialize_database
from database.db import SessionLocal
from database.models import Course, Lecturer, Student, StudentCourse, User


def _get_or_create(db, model, lookup, values):
    instance = db.query(model).filter_by(**lookup).first()
    if instance is None:
        instance = model(**values)
        db.add(instance)
        db.flush()
    return instance


def seed_database():
    """Ensure the minimum demonstration users, staff, courses, and students.

    Existing data is never removed or overwritten, so this function is safe to
    execute before every demo or application start.
    """
    initialize_database()
    db = SessionLocal()
    try:
        _get_or_create(
            db,
            User,
            {"username": "admin"},
            {"username": "admin", "password": "admin123", "role": "Admin"},
        )
        _get_or_create(
            db,
            User,
            {"username": "qa1"},
            {"username": "qa1", "password": "qa123", "role": "QA"},
        )

        jeff = _get_or_create(
            db,
            Lecturer,
            {"email": "jeff@example.com"},
            {
                "full_name": "Mr Jeff",
                "email": "jeff@example.com",
                "department": "Computing",
            },
        )
        _get_or_create(
            db,
            Lecturer,
            {"email": "musoke@example.com"},
            {
                "full_name": "Dr Musoke",
                "email": "musoke@example.com",
                "department": "Computing",
            },
        )

        database_systems = _get_or_create(
            db,
            Course,
            {"course_code": "CSC220"},
            {
                "course_code": "CSC220",
                "course_name": "Database Systems",
                "credit_units": 3,
                "semester": "Semester 1",
            },
        )
        algorithms = _get_or_create(
            db,
            Course,
            {"course_code": "CSC305"},
            {
                "course_code": "CSC305",
                "course_name": "Algorithms",
                "credit_units": 3,
                "semester": "Semester 1",
            },
        )
        accounting = _get_or_create(
            db,
            Course,
            {"course_code": "BIT210"},
            {
                "course_code": "BIT210",
                "course_name": "Computerized Accounting",
                "credit_units": 3,
                "semester": "Semester 1",
            },
        )

        students = {}
        for values in (
            {
                "student_number": "2300100666",
                "index_number": "2026/AUG/CDF/C12256/DIST",
                "full_name": "Kims",
                "admission_year": "2026",
                "intake": "AUG",
                "programme": "CDF",
                "study_mode": "DIST",
                "year_of_study": "Year 1",
            },
            {
                "student_number": "2300100667",
                "index_number": "2022/FEB/DCS/D930256/WK",
                "full_name": "John Smith",
                "admission_year": "2022",
                "intake": "FEB",
                "programme": "DCS",
                "study_mode": "WK",
                "year_of_study": "Year 3",
            },
            {
                "student_number": "2300100668",
                "index_number": "2024/FEB/BIST/B230256/DAY",
                "full_name": "Mary Jane",
                "admission_year": "2024",
                "intake": "FEB",
                "programme": "BIST",
                "study_mode": "DAY",
                "year_of_study": "Year 2",
            },
            {
                "student_number": "2300100669",
                "index_number": "2023/FEB/BCS/B231256/DAY",
                "full_name": "Peter Okello",
                "admission_year": "2023",
                "intake": "FEB",
                "programme": "BCS",
                "study_mode": "DAY",
                "year_of_study": "Year 3",
            },
        ):
            students[values["student_number"]] = _get_or_create(
                db, Student, {"student_number": values["student_number"]}, values
            )

        registrations = (
            (students["2300100666"], database_systems),
            (students["2300100667"], database_systems),
            (students["2300100668"], database_systems),
            (students["2300100666"], algorithms),
            (students["2300100669"], algorithms),
            (students["2300100669"], accounting),
        )
        for student, course in registrations:
            exists = db.query(StudentCourse).filter_by(
                student_id=student.id, course_id=course.id
            ).first()
            if exists is None:
                db.add(StudentCourse(student_id=student.id, course_id=course.id))

        db.commit()
        return {"courses": 3, "lecturers": 2, "students": 4}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    summary = seed_database()
    print(f"Demo data ready: {summary}")
