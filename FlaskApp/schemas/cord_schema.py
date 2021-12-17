from flask.json import dump
from marshmallow import validate
from main import ma
from models.cords import Cord
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Range


class CordSchema(ma.SQLAlchemyAutoSchema):
    cord_id = auto_field(dump_only=True)
    cord_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    material = auto_field()
    thickness = auto_field()
    cost_per_meter = auto_field()

    creator = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    


    class Meta:
        model = Cord
        load_instance = True

cord_schema = CordSchema()
cords_schema = CordSchema(many=True)
