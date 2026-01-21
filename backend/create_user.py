from app import models, database, schemas
from app.core import security
from sqlalchemy.orm import Session

db = database.SessionLocal()

def create_user(username, email, password):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        print(f"User {email} already exists.")
        return

    hashed_password = security.get_password_hash(password)
    new_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    print(f"User {username} created successfully.")

if __name__ == "__main__":
    create_user("admin", "admin@example.com", "password123")
