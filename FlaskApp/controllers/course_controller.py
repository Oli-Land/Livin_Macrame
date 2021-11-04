from flask import Blueprint, jsonify, request
from main import db
from models.courses import Course
from schemas.course_schema import courses_schema, course_schema

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
    return jsonify(courses_schema.dump(courses))

@courses.route("/courses/", methods=["POST"])
def create_course():
    new_course = course_schema.load(request.json)
    db.session.add(new_course)
    db.session.commit()
    return jsonify(course_schema.dump(new_course))

@courses.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course_schema.dump(course))

@courses.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    course = Course.query.filter_by(course_id=id)
    updated_fields = course_schema.dump(request.json)
    if updated_fields:
        course.update(updated_fields)
        db.session.commit()
    return jsonify(course_schema.dump(course.first()))

@courses.route("/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify(course_schema.dump(course))

