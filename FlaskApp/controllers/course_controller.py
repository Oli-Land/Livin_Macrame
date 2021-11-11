from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from main import db
from models.courses import Course
from schemas.course_schema import courses_schema, course_schema


courses = Blueprint('courses', __name__)


### VIEWS ###

# Homepage route endpoint
@courses.route('/')
def home_page():
    data = {
    "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)


# The GET routes endpoint
@courses.route("/courses/", methods=["GET"])
def get_courses():
    data = {
    "page_title": "Course Index",
    "courses": courses_schema.dump(Course.query.all())
    }
    return render_template("course_index.html", page_data=data)

# The POST routes endpoint
@courses.route("/courses/", methods=["POST"])
def create_course():
    new_course = course_schema.load(request.form)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for("courses.get_courses")) 

# The GET specific route endpoint
@courses.route("/courses/<int:id>/", methods=["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    data = {
        "page_title": "Course Detail",
        "course": course_schema.dump(course)
    }
    return render_template("course_detail.html", page_data=data)

# The PUT/PATCH route
@courses.route("/courses/<int:id>/", methods=["POST"])
def update_course(id):

    course = Course.query.filter_by(course_id=id)

    updated_fields = course_schema.dump(request.form)
    if updated_fields:
        course.update(updated_fields)
        db.session.commit()
    
    data = {
        "page_title": "Course Detail",
        "course": course_schema.dump(course.first())
    }
    return render_template("course_detail.html", page_data=data)

# The DELETE endpoint
@courses.route("/courses/<int:id>/delete/", methods=["POST"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("courses.get_courses"))

