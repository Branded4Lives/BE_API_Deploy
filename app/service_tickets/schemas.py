from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Inventory, ServiceTicket


class CustomerNestedSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()


class MechanicNestedSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    specialty = fields.String()


class InventoryNestedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_fk = True
        load_instance = False


class ServiceTicketSchema(SQLAlchemyAutoSchema):
    customer = fields.Nested(CustomerNestedSchema)
    mechanics = fields.List(fields.Nested(MechanicNestedSchema))
    parts = fields.List(fields.Nested(InventoryNestedSchema))

    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = False


class ServiceTicketCreateSchema(Schema):
    customer_id = fields.Integer(required=True)
    vin = fields.String(required=True, validate=validate.Length(min=1, max=17))
    description = fields.String(required=True, validate=validate.Length(min=1))
    service_date = fields.String(load_default=None)
    status = fields.String(load_default="open")
    mechanic_ids = fields.List(fields.Integer(), load_default=list)
    part_ids = fields.List(fields.Integer(), load_default=list)


class ServiceTicketUpdateSchema(Schema):
    customer_id = fields.Integer()
    vin = fields.String(validate=validate.Length(min=1, max=17))
    description = fields.String(validate=validate.Length(min=1))
    service_date = fields.String(allow_none=True)
    status = fields.String()


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
service_ticket_create_schema = ServiceTicketCreateSchema()
service_ticket_update_schema = ServiceTicketUpdateSchema()
