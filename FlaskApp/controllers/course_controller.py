from flask import Blueprint, jsonify, request
from main import db
from models.courses import Course

courses = Blueprint('courses', __name__)



@courses.route('/')
def hello_world():
    return "Hello world!"

@courses.route('/students/')
def get_students():
    return "This will be a list of students "

@courses.route('/students/<int:student_id>/')
def get_specific_students(student_id):
    return f"This will be a page displaying info about {student_id} "





@courses.route("/courses/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.serialize for course in courses])

@courses.route("/courses/", methods=["POST"])
def create_course():
    new_course = Course(request.json['course_name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.serialize)

@courses.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize)

@courses.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    course = Course.query.filter_by(course_id=id)
    course.update(dict(course_name=request.json["course_name"]))
    db.session.commit()
    return jsonify(course.first().serialize)

@courses.route("/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify(course.serialize)

