from flask.json import dump
from marshmallow import validate
from main import ma
from models.projects import Project
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Range

    # Add imported marshmallow validators here
class ProjectSchema(ma.SQLAlchemyAutoSchema):
    # only look for project id if it comes from the database
    project_id = auto_field(dump_only=True)
    project_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    # price = auto_field(required=False, validate=Range(0, 500))
    creator = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )
    """ patterns = ma.Nested(
        "PatternSchema",
        only=("id", "name", "email",)
    ) """

    #metadata about the projectSchema class
    class Meta:
        model = Project
        load_instance = True

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
