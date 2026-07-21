from database.db import SessionLocal
from database.models import AttendanceSession


db = SessionLocal()


sessions = db.query(
    AttendanceSession
).all()


for s in sessions:

    print(
        "ID:",
        s.id,
        "Course:",
        s.course_id,
        "Period:",
        s.period,
        "Date:",
        s.session_date
    )


db.close()