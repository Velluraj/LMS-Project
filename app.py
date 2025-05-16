from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskuser:yourpassword@localhost/portal_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    reg_no = db.Column(db.String(100), unique=True)
    batch = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    staff_code = db.Column(db.String(100), unique=True)
    department = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'student_login':
            email = request.form['student_email']
            password = request.form['student_password']
            student = Student.query.filter_by(email=email, password=password).first()
            if student:
                return f"Welcome, {student.name}!"
            else:
                return "Invalid student credentials."

        elif form_type == 'staff_login':
            code = request.form['staff_code']
            department = request.form['staff_department']
            password = request.form['staff_password']
            staff = Staff.query.filter_by(staff_code=code, department=department, password=password).first()
            if staff:
                return f"Welcome, {staff.name}!"
            else:
                return "Invalid staff credentials."

        elif form_type == 'student_signup':
            name = request.form['student_name']
            reg_no = request.form['student_reg']
            batch = request.form['student_batch']
            email = request.form['student_email_signup']
            password = request.form['student_password_signup']
            confirm = request.form['student_confirm_password']
            if password == confirm:
                new_student = Student(name=name, reg_no=reg_no, batch=batch, email=email, password=password)
                db.session.add(new_student)
                db.session.commit()
                return "Student signed up successfully!"
            else:
                return "Passwords do not match."

        elif form_type == 'staff_signup':
            name = request.form['staff_name']
            staff_code = request.form['staff_code_signup']
            department = request.form['staff_department_signup']
            email = request.form['staff_email']
            password = request.form['staff_password_signup']
            confirm = request.form['staff_confirm_password']
            if password == confirm:
                new_staff = Staff(name=name, staff_code=staff_code, department=department, email=email, password=password)
                db.session.add(new_staff)
                db.session.commit()
                return "Staff signed up successfully!"
            else:
                return "Passwords do not match."

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)
