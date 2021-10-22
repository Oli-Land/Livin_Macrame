from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/students/')
def get_students():
    return "This will be a list of students "

@app.route('/students/<int:student_id>/')
def get_specific_students(student_id):
    return f"This will be a page displaying info about {student_id} "

if __name__ == '__main__':
    app.run(debug=True)