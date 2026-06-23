from attendance.student_service import add_student, get_all_students

add_student("John Doe", "23001", "Computer Science", "Year 1")

students = get_all_students()

for s in students:
    print(s.full_name, s.index_number)