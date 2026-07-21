from attendance.session_summary import get_session_summary



summary = get_session_summary(
    session_id=1
)



print("\n===== ATTENDANCE SUMMARY =====")


print(
    "Present:",
    summary["present_count"]
)


print(
    "Absent:",
    summary["absent_count"]
)



print("\nPRESENT STUDENTS")


for student in summary["present"]:

    print(
        "✓",
        student["name"],
        student["student_number"]
    )



print("\nABSENT STUDENTS")


for student in summary["absent"]:

    print(
        "✗",
        student["name"],
        student["student_number"]
    )