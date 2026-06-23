from database.db import SessionLocal
from database.models import User

db = SessionLocal()

db.query(User).delete()

db.commit()
db.close()

print("All users deleted")