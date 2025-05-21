from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory user storage
students = {
    "student@example.com": {
        "name": "John Doe",
        "batch": "2026",
        "course": "B.Tech CSE",
        "password": "password123",
        "marks": 85,
        "attendance": 92,
        "completion": 80,
        "notifications": ["New assignment posted", "Exam schedule released"]
    }
}
staff_members = {}

# ========== AUTH ==========
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'student_login':
            email = request.form['student_email']
            password = request.form['student_password']
            user = students.get(email)
            if user and user['password'] == password:
                session['user'] = email
                session['role'] = 'student'
                flash('Student login successful!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid student login.', 'error')

        elif form_type == 'student_signup':
            email = request.form['student_email_signup']
            if email in students:
                flash('Student already exists.', 'error')
            elif request.form['student_password_signup'] != request.form['student_confirm_password']:
                flash('Passwords do not match.', 'error')
            else:
                students[email] = {
                    'name': request.form['student_name'],
                    'reg': request.form['student_reg'],
                    'batch': request.form['student_batch'],
                    'course': 'B.Tech CSE',
                    'password': request.form['student_password_signup'],
                    'marks': 0,
                    'attendance': 0,
                    'completion': 0,
                    'notifications': []
                }
                flash('Student signed up successfully.', 'success')

        elif form_type == 'staff_login':
            code = request.form['staff_code']
            dept = request.form['staff_department']
            password = request.form['staff_password']
            for email, staff in staff_members.items():
                if staff['code'] == code and staff['department'] == dept and staff['password'] == password:
                    session['user'] = email
                    session['role'] = 'staff'
                    flash('Staff login successful!', 'success')
                    return redirect(url_for('staff_dashboard'))
            flash('Invalid staff login.', 'error')

        elif form_type == 'staff_signup':
            email = request.form['staff_email']
            if email in staff_members:
                flash('Staff already exists.', 'error')
            elif request.form['staff_password_signup'] != request.form['staff_confirm_password']:
                flash('Passwords do not match.', 'error')
            else:
                staff_members[email] = {
                    'name': request.form['staff_name'],
                    'code': request.form['staff_code_signup'],
                    'department': request.form['staff_department_signup'],
                    'password': request.form['staff_password_signup']
                }
                flash('Staff signed up successfully.', 'success')

    return render_template('index.html')

# ========== STUDENT INTERFACE ==========

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    student = students.get(session['user'])
    return render_template('dashboard.html', student=student)

@app.route('/student/course-content')
def course_content():
    return render_template('course_content.html')

@app.route('/student/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == 'POST':
        file = request.files['assignment']
        if file and file.filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash("Assignment uploaded successfully", "success")
        else:
            flash("Please select a file to upload", "error")
    return render_template('assignment_submission.html')

@app.route('/student/discussion')
def discussion():
    return render_template('discussion.html')

@app.route('/student/grades')
def grades():
    student = students.get(session.get('user'))
    return render_template('grades.html', student=student)

@app.route('/student/notifications')
def notifications():
    student = students.get(session.get('user'))
    return render_template('notifications.html', notifications=student.get("notifications", []))

@app.route('/student/profile')
def profile():
    student = students.get(session.get('user'))
    return render_template('profile.html', student=student)

# ========== STAFF INTERFACE ==========

@app.route('/staff/dashboard')
def staff_dashboard():
    if session.get('role') != 'staff':
        flash('Access denied. Staff only.', 'error')
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/staff/courses')
def course_management():
    return render_template('course_management.html')

@app.route('/staff/content-upload')
def content_upload():
    return render_template('content_upload.html')

@app.route('/staff/schedule')
def class_schedule():
    return render_template('class_schedule.html')

@app.route('/staff/students')
def student_interaction():
    return render_template('student_interaction.html')

@app.route('/staff/profile')
def staff_profile_settings():
    return render_template('profile.html')

# ========== LOGOUT ==========

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# ========== RUN ==========

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
