from attendance.export_report import (
    export_session_csv
)



result = export_session_csv(
    session_id=6,
    filename="CSC220_attendance.csv"
)


print(result)