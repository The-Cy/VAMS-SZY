import csv

from attendance.session_summary import (
    get_session_summary
)



def export_session_csv(
    session_id,
    filename="attendance_report.csv"
):


    summary = get_session_summary(
        session_id
    )


    if not summary:

        return "❌ Session not found"



    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.writer(file)



        # Header

        writer.writerow(
            [
                "Student Number",
                "Student Name",
                "Status"
            ]
        )



        # Present students

        for student in summary["present"]:


            writer.writerow(
                [
                    student["student_number"],
                    student["name"],
                    "Present"
                ]
            )



        # Absent students

        for student in summary["absent"]:


            writer.writerow(
                [
                    student["student_number"],
                    student["name"],
                    "Absent"
                ]
            )



    return (
        f"✅ Report exported successfully: "
        f"{filename}"
    )