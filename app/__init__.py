from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import ValidationError

from config import DevelopmentConfig

from .docs.swagger_spec import build_swagger_spec
from .extensions import db


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL must be set for this environment.")
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set for this environment.")

    db.init_app(app)

    from .customers import customers_bp
    from .inventory import inventory_bp
    from .mechanics import mechanics_bp
    from .service_tickets import service_tickets_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    swagger_ui = get_swaggerui_blueprint(
        "/docs",
        "/swagger.json",
        config={"app_name": "Mechanic Shop API Deployment"},
    )
    app.register_blueprint(swagger_ui, url_prefix="/docs")

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "Mechanic Shop API Deployment",
                "docs": "/docs",
                "swagger": "/swagger.json",
                "resources": {
                    "customers": "/customers",
                    "mechanics": "/mechanics",
                    "service_tickets": "/service-tickets",
                    "inventory": "/inventory",
                },
            }
        )

    @app.get("/swagger.json")
    def swagger_json():
        return jsonify(build_swagger_spec(swagger(app), app))

    @app.cli.command("init-db")
    def init_db():
        db.drop_all()
        db.create_all()
        print("Database initialized.")

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    return app
