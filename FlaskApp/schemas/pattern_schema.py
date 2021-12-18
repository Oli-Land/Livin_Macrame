from flask.json import dump
from marshmallow import validate
from main import ma
from models.patterns import Pattern
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Range

    # Add imported marshmallow validators here
class PatternSchema(ma.SQLAlchemyAutoSchema):
    # only look for project id if it comes from the database
    pattern_id = auto_field(dump_only=True)
    pattern_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    length = auto_field()
    width = auto_field()
    knots_long = auto_field()
    knots_wide = auto_field()
    num_of_cords = auto_field()
    cords_length = auto_field()
    total_cord = auto_field()

    creator = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    knot = ma.Nested(
        "KnotSchema"
    )


    class Meta:
        model = Pattern
        load_instance = True

pattern_schema = PatternSchema()
patterns_schema = PatternSchema(many=True)
