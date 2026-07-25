from attendance.session_loader import (
    get_courses,
    get_lecturers
)


print(
    "COURSES:"
)

print(
    get_courses()
)


print(
    "LECTURERS:"
)

print(
    get_lecturers()
)