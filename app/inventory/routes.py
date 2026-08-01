from flask import jsonify, request

from app.extensions import db
from app.models import Inventory
from app.utils.auth import mechanic_token_required

from . import inventory_bp
from .schemas import (
    inventory_create_schema,
    inventory_items_schema,
    inventory_schema,
    inventory_update_schema,
)


def get_inventory_or_404(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return None, (jsonify({"error": "Inventory part not found"}), 404)
    return part, None


@inventory_bp.post("/")
@mechanic_token_required
def create_inventory_item(mechanic_id):
    data = inventory_create_schema.load(request.get_json() or {})

    if Inventory.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "An inventory item with that name already exists"}), 409

    part = Inventory(**data)
    db.session.add(part)
    db.session.commit()

    return jsonify(inventory_schema.dump(part)), 201


@inventory_bp.get("/")
def get_inventory_items():
    parts = Inventory.query.order_by(Inventory.id).all()
    return jsonify(inventory_items_schema.dump(parts))


@inventory_bp.get("/<int:part_id>")
def get_inventory_item(part_id):
    part, error = get_inventory_or_404(part_id)
    if error:
        return error
    return jsonify(inventory_schema.dump(part))


@inventory_bp.put("/<int:part_id>")
@mechanic_token_required
def update_inventory_item(mechanic_id, part_id):
    part, error = get_inventory_or_404(part_id)
    if error:
        return error

    data = inventory_update_schema.load(request.get_json() or {})

    if "name" in data and data["name"] != part.name:
        if Inventory.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "An inventory item with that name already exists"}), 409

    for key, value in data.items():
        setattr(part, key, value)

    db.session.commit()
    return jsonify(inventory_schema.dump(part))


@inventory_bp.delete("/<int:part_id>")
@mechanic_token_required
def delete_inventory_item(mechanic_id, part_id):
    part, error = get_inventory_or_404(part_id)
    if error:
        return error

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Inventory item deleted successfully"})
