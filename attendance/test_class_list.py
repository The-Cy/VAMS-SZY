from attendance.class_list_service import get_course_students



students = get_course_students(
    course_id=1
)



for student in students:

    print(
        student["name"],
        student["student_number"],
        student["status"]
    )