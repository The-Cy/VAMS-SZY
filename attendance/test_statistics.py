from attendance.attendance_statistics import (
    get_student_attendance_percentage
)



result = get_student_attendance_percentage(
    "2300100666"
)



print("\n===== STUDENT ATTENDANCE =====")


print(
    "Name:",
    result["student_name"]
)


print(
    "Number:",
    result["student_number"]
)


print(
    "Classes:",
    result["total_classes"]
)


print(
    "Attendance:",
    result["attendance_percentage"],
    "%"
)