from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Inventory


class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        include_fk = True
        load_instance = False


class InventoryCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))


class InventoryUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1))
    price = fields.Float(validate=validate.Range(min=0))


inventory_schema = InventorySchema()
inventory_items_schema = InventorySchema(many=True)
inventory_create_schema = InventoryCreateSchema()
inventory_update_schema = InventoryUpdateSchema()
