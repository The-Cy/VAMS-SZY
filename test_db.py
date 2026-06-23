from database.db import SessionLocal
from database.models import Student

db = SessionLocal()

new_student = Student(
    full_name="Test Student",
    index_number="TEST001",
    programme="Computer Science",
    year_of_study="Year 1"
)

db.add(new_student)
db.commit()
db.close()

print("Student inserted successfully!")