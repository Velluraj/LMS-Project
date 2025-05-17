from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory data store
students = {}
staff_members = {}
reset_requests = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # Student login
        if form_type == 'student_login':
            email = request.form['student_email']
            password = request.form['student_password']
            user = students.get(email)
            if user and user['password'] == password:
                flash('Student login successful!', 'success')
            else:
                flash('Invalid student login.', 'error')

        # Student signup
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
                    'password': request.form['student_password_signup']
                }
                flash('Student signed up successfully.', 'success')

        # Staff login
        elif form_type == 'staff_login':
            code = request.form['staff_code']
            dept = request.form['staff_department']
            password = request.form['staff_password']
            for email, staff in staff_members.items():
                if staff['code'] == code and staff['department'] == dept and staff['password'] == password:
                    flash('Staff login successful!', 'success')
                    break
            else:
                flash('Invalid staff login.', 'error')

        # Staff signup
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

        # Password reset verification
        elif form_type == 'reset_password_request':
            user_type = request.form['user_type']
            identifier = request.form['reset_identifier']
            session['reset_email'] = identifier
            session['reset_user_type'] = user_type

            if user_type == 'student' and identifier in students:
                flash('Student verified. Enter new password below.', 'success')
            elif user_type == 'staff' and identifier in staff_members:
                flash('Staff verified. Enter new password below.', 'success')
            else:
                session.pop('reset_email', None)
                session.pop('reset_user_type', None)
                flash('User not found.', 'error')
            return redirect(url_for('index'))

        # Confirm new password
        elif form_type == 'reset_password_confirm':
            email = session.get('reset_email')
            user_type = session.get('reset_user_type')
            new_pass = request.form['new_password']
            confirm_pass = request.form['confirm_password']

            if not email or not user_type:
                flash('Reset session expired.', 'error')
            elif new_pass != confirm_pass:
                flash('Passwords do not match.', 'error')
            else:
                if user_type == 'student' and email in students:
                    students[email]['password'] = new_pass
                    flash('Student password reset successfully.', 'success')
                elif user_type == 'staff' and email in staff_members:
                    staff_members[email]['password'] = new_pass
                    flash('Staff password reset successfully.', 'success')
                else:
                    flash('User not found for reset.', 'error')
                session.pop('reset_email', None)
                session.pop('reset_user_type', None)
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
