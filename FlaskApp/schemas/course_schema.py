from flask.json import dump
from marshmallow import validate
from main import ma
from models.courses import Course
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class CourseSchema(ma.SQLAlchemyAutoSchema):
    # only look for course id if it comes from the database
    course_id = auto_field(dump_only=True)
    # Add imported marshmallow validators here
    course_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))

    #metadata about the CourseSchema class
    class Meta:
        model = Course
        load_instance = True

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
