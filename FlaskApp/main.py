import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

def create_app():
   
    app = Flask(__name__)

    app.config.from_object("config.app_config")
 
    db = SQLAlchemy(app)

    # call it what makes sense for your database
    class Course(db.Model):
        __tablename__ = "courses"
        course_id = db.Column(db.Integer, primary_key=True)
        course_name = db.Column(db.String(80), unique=True, nullable=False)

        def __init__(self, course_name):
            self.course_name = course_name
        
        @property
        def serialize(self):
            return {
                "course_id": self.course_id,
                "course_name": self.course_name
            }

    db.create_all()

    @app.route('/')
    def hello_world():
        return "Hello world!"

    @app.route('/students/')
    def get_students():
        return "This will be a list of students "

    @app.route('/students/<int:student_id>/')
    def get_specific_students(student_id):
        return f"This will be a page displaying info about {student_id} "





    @app.route("/courses/", methods=["GET"])
    def get_courses():
        courses = Course.query.all()
        return jsonify([course.serialize for course in courses])

    @app.route("/courses/", methods=["POST"])
    def create_course():
        new_course = Course(request.json['course_name'])
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.serialize)

    @app.route("/courses/<int:id>/", methods = ["GET"])
    def get_course(id):
        course = Course.query.get_or_404(id)
        return jsonify(course.serialize)

    @app.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
    def update_course(id):
        course = Course.query.filter_by(course_id=id)
        course.update(dict(course_name=request.json["course_name"]))
        db.session.commit()
        return jsonify(course.first().serialize)

    @app.route("/courses/<int:id>/", methods=["DELETE"])
    def delete_course(id):
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return jsonify(course.serialize)



    return app

