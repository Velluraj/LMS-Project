from flask import Flask, render_template, request, redirect, url_for

app = Flask(_name_)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'student_login':
            email = request.form['student_email']
            password = request.form['student_password']
            return f"Student Login - Email: {email}, Password: {password}"
        
        elif form_type == 'staff_login':
            code = request.form['staff_code']
            department = request.form['staff_department']
            password = request.form['staff_password']
            return f"Staff Login - Code: {code}, Dept: {department}, Password: {password}"
        
        elif form_type == 'student_signup':
            return f"Student Signup - {dict(request.form)}"
        
        elif form_type == 'staff_signup':
            return f"Staff Signup - {dict(request.form)}"
    
    return render_template('login.html')

if _name_ == '_main_':
    app.run(debug=True)
