from flask.json import dump
from main import ma
from models.courses import Course
from marshmallow_sqlalchemy import auto_field

class CourseSchema(ma.SQLAlchemyAutoSchema):
    # only look for course id if it comes from the database
    course_id = auto_field(dump_only=True)

    #metadata about the CourseSchema class
    class Meta:
        model = Course
        load_instance = True

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
