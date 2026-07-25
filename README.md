# VAMS-SZY — Voice Attendance Management System

VAMS-SZY is a Python desktop prototype for recording university attendance through offline voice recognition. It allows an authorized user to log in, create a course attendance session, mark registered students present by voice, automatically mark remaining students absent, review previous sessions, and export a CSV report.

This README is the single source of truth for the current system: its architecture, use, database design, development history, limitations, and panel preparation.

## 1. Project objective

Manual attendance takes class time, is difficult to search later, and can create transcription errors. VAMS-SZY provides a structured attendance process:

```text
Login
  -> Admin Dashboard
  -> Create Attendance Session
  -> Voice Attendance Dashboard
  -> Finish Session
  -> Session History / Report / CSV Export
```

The system is a **voice-assisted attendance prototype**. It uses a spoken student number as the main identifier. It is not yet a speaker-biometric identity system; speaker verification is future work.

## 2. Technology choices

| Technology | Use in this project | Why it was chosen |
|---|---|---|
| Python | Main language | Fast development and clear separation of modules. |
| PyQt5 | Desktop GUI | Supplies forms, tables, buttons, dialogs, and event handling. |
| SQLite | Local database | Requires no database server and is suitable for a demonstration on one computer. |
| SQLAlchemy | ORM | Maps Python models to tables and keeps database operations out of GUI code. |
| Vosk | Speech recognition | Works offline, so the demo does not depend on internet access. |
| PyAudio | Microphone audio | Streams microphone audio into Vosk. |
| RapidFuzz | Name comparison | Provides optional soft comparison of a spoken name with the stored name. |

## 3. Installation and starting the application

Project directory:

```text
C:\projies\voice-art\VAMS-SZY
```

Activate the virtual environment if required:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the full application:

```powershell
python -m speech.run_voice
```

`python -m gui.test_session` starts the same complete application flow and is retained as an alternative launcher.

The startup code safely creates missing tables, adds the `session_name` database column to an older database when necessary, and inserts missing demonstration data. It does **not** delete existing attendance records.

### Demonstration login account

```text
Username: admin
Password: admin123
```

This is a prototype account. Password hashing is listed as future security work.

## 4. How to demonstrate the system

1. Run `python -m speech.run_voice`.
2. Log in as `admin` / `admin123`.
3. Select **Create Attendance Session**.
4. Select a course, lecturer, date, and period.
5. Click **Start Attendance**.
6. The attendance dashboard opens with only students registered for the chosen course.
7. Call a student with their name, student number, and status. Example:

   ```text
   Kims two three zero zero one zero zero six six six present
   ```

8. Confirm that the matching student becomes checked, has status `Present`, and receives a time.
9. Finish attendance using the finish command supported by the speech parser.
10. Confirm that students who were not marked present become `Absent`, retain an unchecked box, and show time `-`.
11. Return to the Admin Dashboard and open **Session History** or **Reports**.
12. In Reports, select a session, generate its summary, and export it to CSV.

## 5. User flow and GUI windows

| Window | File | Purpose |
|---|---|---|
| Login | `gui/login_window.py` | Validates a user from the `users` table. |
| Admin Dashboard | `gui/admin_dashboard.py` | Navigation to create session, active attendance, history, reports, and logout. |
| Create Session | `gui/session_window.py` | Selects course, lecturer, date, and period; creates the session. |
| Attendance Dashboard | `gui/attendance_window.py` | Displays registered students and live voice-driven attendance changes. |
| Session History | `gui/session_history.py` | Searchable list of past and active attendance sessions. |
| Session Details | `gui/session_details.py` | Read-only attendance records for one selected session. |
| Reports | `gui/report_window.py` | Session summary, present/absent list, and CSV export. |

The attendance table is intentionally read-only. Users cannot manually edit names, student numbers, status, time, or tick a checkbox. The checkbox is an indicator: checked means `Present`; unchecked means `Waiting` or `Absent`.

## 6. Architecture

```text
                    +-------------------+
                    | PyQt5 Login Window |
                    +---------+---------+
                              |
                    +---------v----------+
                    | Admin Dashboard    |
                    +--+-------+-------+-+
                       |       |       |
       +---------------+       |       +----------------+
       |                       |                        |
+------v-------+      +--------v-------+       +--------v--------+
| Session Window|      | Session History|       | Report Window   |
+------+--------+      +--------+-------+       +--------+--------+
       |                        |                        |
       v                        v                        v
 attendance/session_manager.py        attendance/session_summary.py
       |                               attendance/export_report.py
       v
 attendance/attendance_service.py <---- attendance/voice_controller.py
       ^                                      ^
       |                                      |
 SQLAlchemy / SQLite                     Vosk / microphone
       |
 database/models.py
```

### Separation of responsibilities

* `gui/` only presents windows and tables.
* `attendance/` contains session and attendance business rules.
* `speech/` recognizes sound and produces commands.
* `database/` defines connections, models, migration, and seed data.

This separation makes the system easier to test and improves future maintainability. For example, the GUI does not directly insert attendance records; it calls the attendance service.

## 7. Voice attendance flow

```text
Microphone
  -> speech/voice_thread.py
  -> Vosk recognizer
  -> speech/parser.py
  -> attendance/voice_controller.py
  -> attendance/attendance_service.py
  -> SQLite attendance_records table
  -> gui/attendance_window.py live update
```

When a voice attendance command is received, the attendance service:

1. Confirms there is an active session.
2. Finds the student by student number.
3. Confirms the student is registered for the selected course through `student_courses`.
4. Optionally compares the spoken name with the stored name.
5. Rejects duplicate attendance for that student in the same session.
6. Saves the attendance record.
7. Updates the relevant dashboard row.

On session completion, every registered student with no record is inserted as `Absent`, and the session is marked closed.

## 8. Database design and relationships

Database file:

```text
data/attendance.db
```

| Table | Important fields | Purpose |
|---|---|---|
| `users` | username, password, role | Login accounts. |
| `students` | student_number, index_number, full_name, programme | Student master data. |
| `lecturers` | full_name, email, department | Lecturer information. |
| `courses` | course_code, course_name, semester | Course units. |
| `student_courses` | student_id, course_id | Student-to-course registration. |
| `attendance_sessions` | session_name, course_id, lecturer_id, started_by, session_date, period, closed | A particular attendance event. |
| `attendance_records` | session_id, student_id, status, timestamp | One student's result in one session. |

### Key relationship explanation

One student can take many courses, and one course can have many students. This is a many-to-many relationship, represented correctly by `student_courses`.

```text
Student 1 ---< StudentCourse >--- 1 Course
Course  1 ---< AttendanceSession
AttendanceSession 1 ---< AttendanceRecord >--- 1 Student
```

This registration table is why a student cannot be marked present in a course they are not registered for.

## 9. How demonstration students are added

The current project deliberately removed the incomplete old Manage Students screen because it used PyQt6 and was not part of the working PyQt5 application.

For the current demonstration, students are added through the safe seed module:

```text
database/seed.py
```

It creates missing users, lecturers, courses, students, and registrations without duplicating existing records. Run it manually when needed:

```powershell
python -m database.seed
```

To add a real new student in the current prototype, two pieces of data are required:

1. A row in `students`, including a unique `student_number` and `index_number`.
2. One or more rows in `student_courses` connecting that student to the courses they take.

Example pattern to add in `database/seed.py`:

```python
new_student = _get_or_create(
    db,
    Student,
    {"student_number": "2300100670"},
    {
        "student_number": "2300100670",
        "index_number": "2026/AUG/BCS/0001/DAY",
        "full_name": "New Student",
        "admission_year": "2026",
        "intake": "AUG",
        "programme": "BCS",
        "study_mode": "DAY",
        "year_of_study": "Year 1",
    },
)
```

Then register the student to a course:

```python
db.add(StudentCourse(student_id=new_student.id, course_id=database_systems.id))
```

The next safe enhancement is a proper PyQt5 student-management module with validation and course-registration controls. It should not be rushed into the presentation build.

## 10. Reporting

Existing report services are reused; report logic was not recreated in the GUI.

| File | Responsibility |
|---|---|
| `attendance/session_summary.py` | Builds present and absent lists plus counts for one session. |
| `attendance/export_report.py` | Writes a selected session to CSV. |
| `attendance/attendance_statistics.py` | Calculates a student's attendance percentage. |
| `gui/report_window.py` | Lets the user choose a session, view the summary, and export CSV. |

CSV is currently supported. PDF, Excel, course filter, and date-range filter are future enhancements.

## 11. Safe database setup and seed data

| File | Purpose |
|---|---|
| `database/bootstrap.py` | Creates missing tables and safely adds the missing `session_name` column to older SQLite databases. |
| `database/seed.py` | Inserts only missing demo data; it does not delete existing data. |
| `database/db.py` | Configures SQLAlchemy engine, session factory, and base model. |
| `database/models.py` | Defines the database tables and relationships. |

The original destructive user-reset and duplicate seed utilities were removed because they were unsafe or no longer used.

## 12. Issues encountered and solutions

| Issue | Root cause | Solution |
|---|---|---|
| Missing `session_name` column | Updating a SQLAlchemy model does not alter an existing SQLite table automatically. | Added `database/bootstrap.py` with a safe additive migration. |
| Empty course and lecturer lists | Reference data had not been inserted. | Added idempotent `database/seed.py`. |
| Duplicate seed data risk | Old seed script inserted records every time. | New seed logic uses get-or-create behavior. |
| Session form did not open voice attendance dashboard | The old test form was standalone. | Main startup and test launcher now use the integrated application flow. |
| Attendance session close error | SQLAlchemy object was accessed after its database session closed. | Stored the session name before closing the connection. |
| Absent students were checked | The GUI assigned `Checked` to absent rows. | Absent rows now remain unchecked and show `Absent` with `-` time. |
| Manual table editing was possible | Standard table items are editable by default. | Dashboard cells and checkboxes are display-only. |
| Old login/dashboard/student screens conflicted | They used PyQt6 and obsolete prototype service calls. | Removed them and replaced them with active PyQt5 windows. |

## 13. Files intentionally removed

The following were obsolete, duplicate, unsafe, or not used by the active application and were removed:

```text
gui/login.py
gui/dashboard.py
gui/student_window.py
gui/test_gui.py
attendance/student_service.py
create_db.py
seed_data.py
fix_users.py
test_user.py
test_students.py
test_db.py
test_attendance.py
```

The focused attendance, speech, report, database, and GUI modules remain.

## 14. Current limitations and honest scope

* Passwords are plain text in this prototype; production must hash passwords with bcrypt or an equivalent algorithm.
* The system recognizes a spoken student number but does not yet verify the speaker by voiceprint.
* SQLite is intended for the local prototype; a multi-user deployment needs a server database, backups, and access control.
* Report filtering by course and date range, PDF/Excel output, audit logs, and detailed roles are not completed.
* The current system has no student-management GUI because the obsolete incomplete version was removed. Demo students are maintained through the seed module.

These are valid future-work points, not claims that the prototype already solves every production requirement.

## 15. Panel questions and answers

### Why use voice attendance?

It reduces manual roll-call time, records attendance immediately, and uses an ordinary microphone. Vosk allows the prototype to work without internet access.

### How do you stop an unregistered student being marked?

The attendance service checks the `student_courses` table before saving attendance. A student number is accepted only if it is registered for the course in the selected session.

### How do you prevent duplicate attendance?

Before inserting a record, the attendance service checks whether that student already has a record in the same attendance session.

### What happens to students not called?

On session completion, the service writes `Absent` records for registered students who do not yet have a record. Their dashboard checkbox remains unchecked.

### Is this a biometric security system?

No. It is a voice-assisted attendance prototype. The student number is the primary identifier. Speaker verification is future work.

### Why SQLite and SQLAlchemy?

SQLite makes the prototype easy to run locally. SQLAlchemy keeps table relationships and database operations structured and makes a later move to a server database easier.

### What would be done before university deployment?

Password hashing, richer role permissions, audit logging, database backups, central database hosting, authorized correction controls, accuracy testing, and stronger identity verification.

## 16. Two-person presentation split

**Presenter 1 — problem and user journey**

Explain the manual-attendance problem, login, dashboard, creating a session, and demonstrate calling a student.

**Presenter 2 — design and implementation**

Explain the architecture, Vosk/offline choice, database relationships, course-registration validation, duplicate prevention, reports, limitations, and future work.

Both presenters should know the limitations section and avoid claiming that speaker verification or password hashing already exists.

## 17. Pre-presentation checklist

1. Activate `.venv` if needed.
2. Run `python -m database.seed`.
3. Confirm microphone permissions in Windows.
4. Run `python -m speech.run_voice`.
5. Log in with `admin` / `admin123`.
6. Test one voice command in a quiet room.
7. Have a dashboard screenshot or recorded fallback in case microphone conditions are poor.
8. Keep this README open for terminology and panel answers.

## 18. Next safe development priorities

1. Add a visible microphone/listening indicator.
2. Add authorized manual attendance override for recognition failure.
3. Build a proper PyQt5 student-management and course-registration module.
4. Add report filtering by course/date and PDF/Excel export.
5. Add bcrypt password hashing and role-based permissions.
6. Add audit logs for login, session creation, session close, changes, and report export.

Do not rebuild the completed voice-attendance path while adding these improvements. Keep GUI, speech, attendance business logic, and database code separate.
