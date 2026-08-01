from flask import jsonify, request

from app.extensions import db
from app.models import Customer, ServiceTicket
from app.service_tickets.schemas import service_tickets_schema
from app.utils.auth import encode_customer_token, token_required

from . import customers_bp
from .schemas import (
    customer_schema,
    customer_update_schema,
    customers_schema,
    login_schema,
)


def get_customer_or_404(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return None, (jsonify({"error": "Customer not found"}), 404)
    return customer, None


@customers_bp.post("/")
def create_customer():
    data = customer_schema.load(request.get_json() or {})

    if Customer.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "A customer with that email already exists"}), 409

    password = data.pop("password")
    customer = Customer(**data)
    customer.set_password(password)
    db.session.add(customer)
    db.session.commit()

    return jsonify(customer_schema.dump(customer)), 201


@customers_bp.post("/login")
def login_customer():
    data = login_schema.load(request.get_json() or {})
    customer = Customer.query.filter_by(email=data["email"]).first()

    if not customer or not customer.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"customer_id": customer.id, "token": encode_customer_token(customer.id)})


@customers_bp.get("/")
def get_customers():
    customers = Customer.query.order_by(Customer.id).all()
    return jsonify(customers_schema.dump(customers))


@customers_bp.get("/my-tickets")
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).order_by(
        ServiceTicket.id
    )
    return jsonify(service_tickets_schema.dump(tickets.all()))


@customers_bp.get("/<int:customer_id>")
def get_customer(customer_id):
    customer, error = get_customer_or_404(customer_id)
    if error:
        return error
    return jsonify(customer_schema.dump(customer))


@customers_bp.put("/<int:customer_id>")
@token_required
def update_customer(auth_customer_id, customer_id):
    if auth_customer_id != customer_id:
        return jsonify({"error": "You can only update your own account"}), 403

    customer, error = get_customer_or_404(customer_id)
    if error:
        return error

    data = customer_update_schema.load(request.get_json() or {})

    if "email" in data and data["email"] != customer.email:
        if Customer.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "A customer with that email already exists"}), 409

    if "password" in data:
        customer.set_password(data.pop("password"))

    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return jsonify(customer_schema.dump(customer))


@customers_bp.delete("/<int:customer_id>")
@token_required
def delete_customer(auth_customer_id, customer_id):
    if auth_customer_id != customer_id:
        return jsonify({"error": "You can only delete your own account"}), 403

    customer, error = get_customer_or_404(customer_id)
    if error:
        return error

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})
