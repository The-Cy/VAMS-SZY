from database.db import engine, Base
from database import models

# This creates all tables in the database
Base.metadata.create_all(bind=engine)

print("Database created successfully!")