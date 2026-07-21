from database.db import SessionLocal
from database.models import (
    User,
    Student,
    Lecturer,
    Course,
    StudentCourse
)


def seed():

    db = SessionLocal()


    print("🌱 Adding sample data...")


    # ============================
    # USERS
    # ============================

    admin = User(
        username="admin",
        password="admin123",
        role="Admin"
    )


    qa = User(
        username="qa1",
        password="qa123",
        role="QA"
    )


    db.add_all([
        admin,
        qa
    ])



    # ============================
    # LECTURERS
    # ============================

    lecturer1 = Lecturer(
        full_name="Mr Jeff",
        email="jeff@example.com",
        department="Computing"
    )


    lecturer2 = Lecturer(
        full_name="Dr Musoke",
        email="musoke@example.com",
        department="Computing"
    )


    db.add_all([
        lecturer1,
        lecturer2
    ])



    # ============================
    # COURSE UNITS
    # ============================

    database = Course(
        course_code="CSC220",
        course_name="Database Systems",
        credit_units=3,
        semester="Semester 1"
    )


    algorithms = Course(
        course_code="CSC305",
        course_name="Algorithms",
        credit_units=3,
        semester="Semester 1"
    )


    accounting = Course(
        course_code="BIT210",
        course_name="Computerized Accounting",
        credit_units=3,
        semester="Semester 1"
    )


    db.add_all([
        database,
        algorithms,
        accounting
    ])


    db.commit()



    # ============================
    # STUDENTS
    # ============================

    student1 = Student(
        student_number="2300100666",
        index_number="2026/AUG/CDF/C12256/DIST",
        admission_year="2026",
        intake="AUG",
        programme="CDF",
        study_mode="DIST",
        full_name="Kims",
        year_of_study="Year 1"
    )


    student2 = Student(
        student_number="2300100667",
        index_number="2022/FEB/DCS/D930256/WK",
        admission_year="2022",
        intake="FEB",
        programme="DCS",
        study_mode="WK",
        full_name="John Smith",
        year_of_study="Year 3"
    )


    student3 = Student(
        student_number="2300100668",
        index_number="2024/FEB/BIST/B230256/DAY",
        admission_year="2024",
        intake="FEB",
        programme="BIST",
        study_mode="DAY",
        full_name="Mary Jane",
        year_of_study="Year 2"
    )


    student4 = Student(
        student_number="2300100669",
        index_number="2023/FEB/BCS/B231256/DAY",
        admission_year="2023",
        intake="FEB",
        programme="BCS",
        study_mode="DAY",
        full_name="Peter Okello",
        year_of_study="Year 3"
    )


    db.add_all([
        student1,
        student2,
        student3,
        student4
    ])

    db.commit()



    # ============================
    # REGISTER STUDENTS TO COURSES
    # ============================

    registrations = [

        # Database Systems
        StudentCourse(
            student_id=student1.id,
            course_id=database.id
        ),

        StudentCourse(
            student_id=student2.id,
            course_id=database.id
        ),

        StudentCourse(
            student_id=student3.id,
            course_id=database.id
        ),


        # Algorithms
        StudentCourse(
            student_id=student1.id,
            course_id=algorithms.id
        ),

        StudentCourse(
            student_id=student4.id,
            course_id=algorithms.id
        ),


        # Accounting
        StudentCourse(
            student_id=student4.id,
            course_id=accounting.id
        )

    ]


    db.add_all(registrations)


    db.commit()


    print("✅ Sample data inserted successfully")


    db.close()



if __name__ == "__main__":
    seed()