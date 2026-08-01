from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Mechanic


class MechanicSchema(SQLAlchemyAutoSchema):
    password = fields.String(load_only=True, required=True)

    class Meta:
        model = Mechanic
        exclude = ("password_hash",)
        include_fk = True
        load_instance = False


class MechanicUpdateSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    email = fields.Email()
    password = fields.String(validate=validate.Length(min=6))
    phone = fields.String(allow_none=True)
    specialty = fields.String(allow_none=True)


class MechanicLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
mechanic_update_schema = MechanicUpdateSchema()
mechanic_login_schema = MechanicLoginSchema()
