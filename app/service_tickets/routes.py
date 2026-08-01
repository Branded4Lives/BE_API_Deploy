from flask import jsonify, request

from app.extensions import db
from app.models import Customer, Inventory, Mechanic, ServiceTicket
from app.utils.auth import mechanic_token_required

from . import service_tickets_bp
from .schemas import (
    service_ticket_create_schema,
    service_ticket_schema,
    service_ticket_update_schema,
    service_tickets_schema,
)


def get_ticket_or_404(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return None, (jsonify({"error": "Service ticket not found"}), 404)
    return ticket, None


def get_mechanic_or_404(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return None, (jsonify({"error": "Mechanic not found"}), 404)
    return mechanic, None


def get_part_or_404(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return None, (jsonify({"error": "Inventory part not found"}), 404)
    return part, None


@service_tickets_bp.post("/")
@mechanic_token_required
def create_service_ticket(mechanic_id):
    data = service_ticket_create_schema.load(request.get_json() or {})

    if not db.session.get(Customer, data["customer_id"]):
        return jsonify({"error": "Customer not found"}), 404

    mechanic_ids = data.pop("mechanic_ids", [])
    part_ids = data.pop("part_ids", [])
    ticket = ServiceTicket(**data)

    for assigned_mechanic_id in mechanic_ids:
        mechanic = db.session.get(Mechanic, assigned_mechanic_id)
        if not mechanic:
            return jsonify({"error": f"Mechanic {assigned_mechanic_id} not found"}), 404
        ticket.mechanics.append(mechanic)

    for part_id in part_ids:
        part = db.session.get(Inventory, part_id)
        if not part:
            return jsonify({"error": f"Inventory part {part_id} not found"}), 404
        ticket.parts.append(part)

    db.session.add(ticket)
    db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 201


@service_tickets_bp.get("/")
def get_service_tickets():
    tickets = ServiceTicket.query.order_by(ServiceTicket.id).all()
    return jsonify(service_tickets_schema.dump(tickets))


@service_tickets_bp.get("/<int:ticket_id>")
def get_service_ticket(ticket_id):
    ticket, error = get_ticket_or_404(ticket_id)
    if error:
        return error
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.put("/<int:ticket_id>")
@mechanic_token_required
def update_service_ticket(mechanic_id, ticket_id):
    ticket, error = get_ticket_or_404(ticket_id)
    if error:
        return error

    data = service_ticket_update_schema.load(request.get_json() or {})

    if "customer_id" in data and not db.session.get(Customer, data["customer_id"]):
        return jsonify({"error": "Customer not found"}), 404

    for key, value in data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@mechanic_token_required
def assign_mechanic(auth_mechanic_id, ticket_id, mechanic_id):
    ticket, ticket_error = get_ticket_or_404(ticket_id)
    if ticket_error:
        return ticket_error

    mechanic, mechanic_error = get_mechanic_or_404(mechanic_id)
    if mechanic_error:
        return mechanic_error

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
@mechanic_token_required
def remove_mechanic(auth_mechanic_id, ticket_id, mechanic_id):
    ticket, ticket_error = get_ticket_or_404(ticket_id)
    if ticket_error:
        return ticket_error

    mechanic, mechanic_error = get_mechanic_or_404(mechanic_id)
    if mechanic_error:
        return mechanic_error

    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.put("/<int:ticket_id>/add-part/<int:part_id>")
@mechanic_token_required
def add_part_to_ticket(mechanic_id, ticket_id, part_id):
    ticket, ticket_error = get_ticket_or_404(ticket_id)
    if ticket_error:
        return ticket_error

    part, part_error = get_part_or_404(part_id)
    if part_error:
        return part_error

    if part not in ticket.parts:
        ticket.parts.append(part)

    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket))


@service_tickets_bp.delete("/<int:ticket_id>")
@mechanic_token_required
def delete_service_ticket(mechanic_id, ticket_id):
    ticket, error = get_ticket_or_404(ticket_id)
    if error:
        return error

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"})
