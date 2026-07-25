"""Safe development bootstrap for the VAMS SQLite database.

This module deliberately does not delete the database.  It creates missing
tables and performs the one additive migration currently required by the
project: ``attendance_sessions.session_name``.
"""

from sqlalchemy import inspect, text

from database.db import Base, engine
from database import models  # noqa: F401 - registers all SQLAlchemy models


def initialize_database():
    """Create tables and apply safe, additive SQLite schema upgrades."""
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    columns = {
        column["name"]
        for column in inspector.get_columns("attendance_sessions")
    }

    if "session_name" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE attendance_sessions "
                    "ADD COLUMN session_name VARCHAR"
                )
            )
            connection.execute(
                text(
                    "UPDATE attendance_sessions "
                    "SET session_name = 'Legacy attendance session' "
                    "WHERE session_name IS NULL"
                )
            )


if __name__ == "__main__":
    initialize_database()
    print("Database schema is ready.")
