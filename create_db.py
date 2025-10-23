from app import app, db, Student

with app.app_context():
    db.create_all()
    print("Database created successfully!")
