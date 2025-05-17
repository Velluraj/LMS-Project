from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/courses')
def course_management():
    return render_template('course_management.html')

@app.route('/content-upload')
def content_upload():
    return render_template('content_upload.html')

@app.route('/schedule')
def class_schedule():
    return render_template('class_schedule.html')

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/students')
def student_interaction():
    return render_template('student_interaction.html')

@app.route('/profile')
def profile_settings():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
