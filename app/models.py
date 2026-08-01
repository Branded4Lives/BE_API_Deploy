from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


service_ticket_mechanics = db.Table(
    "service_ticket_mechanics",
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_tickets.id"),
        primary_key=True,
    ),
    db.Column(
        "mechanic_id",
        db.Integer,
        db.ForeignKey("mechanics.id"),
        primary_key=True,
    ),
)


service_ticket_inventory = db.Table(
    "service_ticket_inventory",
    db.Column(
        "service_ticket_id",
        db.Integer,
        db.ForeignKey("service_tickets.id"),
        primary_key=True,
    ),
    db.Column(
        "inventory_id",
        db.Integer,
        db.ForeignKey("inventory.id"),
        primary_key=True,
    ),
)


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30))
    address = db.Column(db.String(255))

    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30))
    specialty = db.Column(db.String(120))

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_mechanics,
        back_populates="mechanics",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_inventory,
        back_populates="parts",
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False,
    )
    vin = db.Column(db.String(17), nullable=False)
    description = db.Column(db.Text, nullable=False)
    service_date = db.Column(db.String(20))
    status = db.Column(db.String(40), nullable=False, default="open")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    customer = db.relationship("Customer", back_populates="service_tickets")
    mechanics = db.relationship(
        "Mechanic",
        secondary=service_ticket_mechanics,
        back_populates="service_tickets",
    )
    parts = db.relationship(
        "Inventory",
        secondary=service_ticket_inventory,
        back_populates="service_tickets",
    )
