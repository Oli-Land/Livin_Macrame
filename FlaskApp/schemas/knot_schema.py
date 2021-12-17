from main import ma
from models.knots import Knot
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Range


class KnotSchema(ma.SQLAlchemyAutoSchema):
    knot_id = auto_field(dump_only=True)
    knot_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    length = auto_field()
    width = auto_field()
    num_of_cords = auto_field()
    cords_length = auto_field()
    total_cord = auto_field()

    creator = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )
    cord = ma.Nested(
        "CordSchema"
    )


    class Meta:
        model = Knot
        load_instance = True

knot_schema = KnotSchema()
knots_schema = KnotSchema(many=True)
