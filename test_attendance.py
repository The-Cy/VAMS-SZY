from attendance.attendance_service import create_session, mark_attendance

# create session
session_id = create_session(course_id=1, period="Morning")

print("Session ID:", session_id)

# mark attendance
result = mark_attendance(session_id, "23001")
print(result)