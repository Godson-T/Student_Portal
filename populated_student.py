from faker import Faker
import random
from app import app, db
from app import Student  # make sure your Student model is imported

# Initialize Faker
fake = Faker()

# Define course and year lists
courses = ["AI", "CSE", "ECE", "MECH", "CIVIL", "EEE","DS"]
years = ["I", "II", "III", "IV"]

# Flask app context (required for db operations)
with app.app_context():
    students = []
    for _ in range(1000):  # 🔁 change 100 to any number you want
        name = fake.name()
        email = fake.email()
        course = random.choice(courses)
        year = random.choice(years)
        student = Student(name=name, email=email, course=course, year=year)
        students.append(student)
    
    # Add all at once for performance
    db.session.add_all(students)
    db.session.commit()
    print(f"✅ {len(students)} fake students added successfully!")
