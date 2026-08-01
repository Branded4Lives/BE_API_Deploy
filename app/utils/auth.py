from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import current_app, jsonify, request
from jose import JWTError, jwt

ALGORITHM = "HS256"


def encode_customer_token(customer_id):
    payload = {
        "customer_id": customer_id,
        "role": "customer",
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=ALGORITHM)


def encode_mechanic_token(mechanic_id):
    payload = {
        "mechanic_id": mechanic_id,
        "role": "mechanic",
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm=ALGORITHM)


def get_bearer_token():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    return auth_header.split(" ", 1)[1].strip()


def token_required(route_function):
    @wraps(route_function)
    def decorated(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({"error": "Bearer token is required"}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=[ALGORITHM],
            )
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        if payload.get("role") != "customer" or "customer_id" not in payload:
            return jsonify({"error": "Customer token is required"}), 403

        return route_function(payload["customer_id"], *args, **kwargs)

    return decorated


def mechanic_token_required(route_function):
    @wraps(route_function)
    def decorated(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({"error": "Bearer token is required"}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=[ALGORITHM],
            )
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        if payload.get("role") != "mechanic" or "mechanic_id" not in payload:
            return jsonify({"error": "Mechanic token is required"}), 403

        return route_function(payload["mechanic_id"], *args, **kwargs)

    return decorated
