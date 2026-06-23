from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file (will be auto-created)
DATABASE_URL = "sqlite:///data/attendance.db"

# Create engine (connects Python to database)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + GUI apps
)

# Session factory (used to talk to DB)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all tables
Base = declarative_base()