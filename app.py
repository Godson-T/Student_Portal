from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50),nullable=False)
    course=db.Column(db.String(50),nullable=False)
    year=db.Column(db.String(5),nullable=False)

@app.route('/add_students')
def add_students():
    return render_template("add_student.html")

    


if __name__ == "__main__":
    app.run(debug=True)