from database.db import SessionLocal
from database.models import User

db = SessionLocal()

existing = db.query(User).filter(User.username == "admin").first()

if not existing:
    user = User(username="admin", password="admin", role="Admin")
    db.add(user)
    db.commit()
    print("Created")
else:
    print("Already exists")

db.close()