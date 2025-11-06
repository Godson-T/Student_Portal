from flask import Flask, redirect, render_template,request,session,flash  # noqa: F401
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from sqlalchemy import func
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


app=Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'  # 🔑 change this to something secure later

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(db.Model,UserMixin):
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
    return render_template("home.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
@app.route("/dashboard")
@login_required
def dashboard():
    recent_added=Student.query.order_by(Student.id.desc()).limit(5).all()
    total_student=Student.query.count()
    total_courses=Student.query.distinct(Student.course).count()
    data = db.session.query(Student.course, func.count(Student.id)).group_by(Student.course).all()
    courses = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    return render_template("dashboard.html",courses=courses, counts=counts,total_student=total_student,total_courses=total_courses, recent_added=recent_added)


@app.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
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

def send_otp(to_email, otp):
    sender_email = "godsont259@gmail.com"
    sender_pass = "gtxu mgkt vuhl yilj"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "OTP Verification"
    msg["From"] = sender_email
    msg["To"] = to_email
    body = f"Your OTP code is: {otp}"
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, to_email,msg.as_string())
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = None

    if request.method=='POST':
        email_input=request.form['email']
        password_input=request.form['password']
        user = User.query.filter_by(email=email_input).first()
        if user and user.check_password(password_input):
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            session['pending_user'] = user.id
            Thread(target=send_otp, args=(email_input, otp)).start()

            return redirect('verify_otp')
        else:
            error_msg="USER NOT FOUND"
            
    return render_template('login.html',error_msg=error_msg)

@app.route("/verify_otp" ,methods=['GET','POST'])
def verify_otp():
    if request.method=='POST':
        entered_otp=request.form.get('otp', '').strip()
        stored_otp = str(session.get('otp', '')).strip()
        if entered_otp==stored_otp:
            user_id=session['pending_user']
            user=User.query.get(user_id)

            login_user(user)
            session.pop('otp', None)
            session.pop('pending_user', None)
            flash("User login successfull","success")
            return redirect('/dashboard')
        else:
            flash("Incorrect OTP. Try again.", "danger")
            return redirect('/verify_otp')
    return render_template('verify_otp.html')
   
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/view_students')
def view_student():
    student=Student.query.all()
    return render_template('view_student.html',students=student)


def send_welcome_email(to_email, student_name, course):
    sender_email = "godsont259@gmail.com"
    sender_pass = "gtxu mgkt vuhl yilj"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🎉 Welcome to Student Portal!"
    msg["From"] = sender_email
    msg["To"] = to_email

    html_content = open("templates/email_temp.html").read()
    html_content = html_content.replace("{{ student_name }}", student_name)
    html_content = html_content.replace("{{ course }}", course)
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, to_email, msg.as_string())

@app.route('/add_students',methods=['GET', 'POST'])
@login_required
def add_students():
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']
        year=request.form['year']
        
        new_student = Student(name=name,email=email,course=course,year=year)
        db.session.add(new_student)
        Thread(target=send_welcome_email, args=(email, name,course)).start()
        db.session.commit()
        
        return redirect('view_students') 
    
    return render_template("add_student.html")



@app.route("/student/<int:id>")
def student_details(id):
    student=Student.query.get_or_404(id)
    return render_template("student.html",student=student)




if __name__ == "__main__":
    app.run(debug=True)