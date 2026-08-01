from flask import jsonify, request

from app.extensions import db
from app.models import Mechanic
from app.utils.auth import encode_mechanic_token, mechanic_token_required

from . import mechanics_bp
from .schemas import (
    mechanic_login_schema,
    mechanic_schema,
    mechanic_update_schema,
    mechanics_schema,
)


def get_mechanic_or_404(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return None, (jsonify({"error": "Mechanic not found"}), 404)
    return mechanic, None


@mechanics_bp.post("/")
def create_mechanic():
    data = mechanic_schema.load(request.get_json() or {})

    if Mechanic.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "A mechanic with that email already exists"}), 409

    password = data.pop("password")
    mechanic = Mechanic(**data)
    mechanic.set_password(password)
    db.session.add(mechanic)
    db.session.commit()

    return jsonify(mechanic_schema.dump(mechanic)), 201


@mechanics_bp.post("/login")
def login_mechanic():
    data = mechanic_login_schema.load(request.get_json() or {})
    mechanic = Mechanic.query.filter_by(email=data["email"]).first()

    if not mechanic or not mechanic.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"mechanic_id": mechanic.id, "token": encode_mechanic_token(mechanic.id)})


@mechanics_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.order_by(Mechanic.id).all()
    return jsonify(mechanics_schema.dump(mechanics))


@mechanics_bp.get("/<int:mechanic_id>")
def get_mechanic(mechanic_id):
    mechanic, error = get_mechanic_or_404(mechanic_id)
    if error:
        return error
    return jsonify(mechanic_schema.dump(mechanic))


@mechanics_bp.put("/<int:mechanic_id>")
@mechanic_token_required
def update_mechanic(auth_mechanic_id, mechanic_id):
    if auth_mechanic_id != mechanic_id:
        return jsonify({"error": "You can only update your own mechanic account"}), 403

    mechanic, error = get_mechanic_or_404(mechanic_id)
    if error:
        return error

    data = mechanic_update_schema.load(request.get_json() or {})

    if "email" in data and data["email"] != mechanic.email:
        if Mechanic.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "A mechanic with that email already exists"}), 409

    if "password" in data:
        mechanic.set_password(data.pop("password"))

    for key, value in data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic))


@mechanics_bp.delete("/<int:mechanic_id>")
@mechanic_token_required
def delete_mechanic(auth_mechanic_id, mechanic_id):
    if auth_mechanic_id != mechanic_id:
        return jsonify({"error": "You can only delete your own mechanic account"}), 403

    mechanic, error = get_mechanic_or_404(mechanic_id)
    if error:
        return error

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"})
