from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Customer


class CustomerSchema(SQLAlchemyAutoSchema):
    password = fields.String(load_only=True, required=True)

    class Meta:
        model = Customer
        exclude = ("password_hash",)
        include_fk = True
        load_instance = False


class CustomerUpdateSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    email = fields.Email()
    password = fields.String(validate=validate.Length(min=6))
    phone = fields.String(allow_none=True)
    address = fields.String(allow_none=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_update_schema = CustomerUpdateSchema()
login_schema = LoginSchema()
