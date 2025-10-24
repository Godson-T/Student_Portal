from flask import Flask, redirect, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50),nullable=False)
    course=db.Column(db.String(50),nullable=False)
    year=db.Column(db.String(5),nullable=False)

@app.route('/')
def home():
    return render_template("layout.html")



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student=Student.query.get_or_404(id)
    if request.method== 'POST' :
        student.name=request.form['name']
        student.email=request.form['email'] 
        student.course=request.form['course'] 
        student.year=request.form['year'] 
        db.session.commit()
        return redirect('/view_students')
    
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_student(id):
    student=Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/view_students')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if  request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user=User(username=username,email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = None

    if request.method=='POST':
        email_input=request.form['email']
        password_input=request.form['password']
        user = User.query.filter_by(email=email_input).first()
        if user and user.check_password(password_input):
            return redirect("/")
        else:
            error_msg="USER NOT FOUND"
            
    return render_template('login.html',error_msg=error_msg)
    #start debug here
    
    
    
@app.route('/view_students')
def view_student():
    student=Student.query.all()
    return render_template('view_student.html',students=student)


@app.route('/add_students',methods=['GET', 'POST'])
def add_students():
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']
        year=request.form['year']
        
        new_student = Student(name=name,email=email,course=course,year=year)
        db.session.add(new_student)
        db.session.commit()
        return redirect('view_students') 
    
    return render_template("add_student.html")

    


if __name__ == "__main__":
    app.run(debug=True)