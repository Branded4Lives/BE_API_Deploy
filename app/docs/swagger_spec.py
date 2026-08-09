def bearer_security():
    return [{"Bearer": []}]


def body_parameter(definition_name):
    return [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": f"#/definitions/{definition_name}"},
        }
    ]


def id_parameter(name, description):
    return {
        "name": name,
        "in": "path",
        "required": True,
        "type": "integer",
        "description": description,
    }


def response(description, definition_name=None, example=None):
    response_data = {"description": description}

    if definition_name:
        response_data["schema"] = {"$ref": f"#/definitions/{definition_name}"}

    if example is not None:
        response_data["examples"] = {"application/json": example}

    return response_data


def build_swagger_spec(base_spec, app=None):
    if app:
        host = app.config.get("SWAGGER_HOST") or "127.0.0.1:5000"
        scheme = app.config.get("SWAGGER_SCHEME") or "http"
    else:
        host = "127.0.0.1:5000"
        scheme = "http"

    base_spec.update(
        {
            "swagger": "2.0",
            "info": {
                "title": "Mechanic Shop API Deployment",
                "description": "Mechanic shop API documented with Swagger, tested with unittest, and configured for Render deployment.",
                "version": "1.0.0",
            },
            "host": host,
            "basePath": "/",
            "schemes": [scheme],
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Use format: Bearer <token>",
                }
            },
            "definitions": definitions(),
            "paths": paths(),
        }
    )
    return base_spec


def definitions():
    return {
        "CustomerPayload": {
            "type": "object",
            "required": ["first_name", "last_name", "email", "password"],
            "properties": {
                "first_name": {"type": "string", "example": "Brandon"},
                "last_name": {"type": "string", "example": "Customer"},
                "email": {"type": "string", "example": "brandon@example.com"},
                "password": {"type": "string", "example": "password123"},
                "phone": {"type": "string", "example": "555-0100"},
                "address": {"type": "string", "example": "123 Main St"},
            },
        },
        "CustomerUpdatePayload": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string", "example": "Brandon"},
                "last_name": {"type": "string", "example": "Updated"},
                "email": {"type": "string", "example": "updated@example.com"},
                "password": {"type": "string", "example": "newpass123"},
                "phone": {"type": "string", "example": "555-0199"},
                "address": {"type": "string", "example": "456 Updated Ave"},
            },
        },
        "CustomerResponse": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "first_name": {"type": "string", "example": "Brandon"},
                "last_name": {"type": "string", "example": "Customer"},
                "email": {"type": "string", "example": "brandon@example.com"},
                "phone": {"type": "string", "example": "555-0100"},
                "address": {"type": "string", "example": "123 Main St"},
            },
        },
        "LoginPayload": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "example": "brandon@example.com"},
                "password": {"type": "string", "example": "password123"},
            },
        },
        "LoginResponse": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "example": "eyJhbGciOi..."},
                "customer_id": {"type": "integer", "example": 1},
                "mechanic_id": {"type": "integer", "example": 1},
            },
        },
        "MechanicPayload": {
            "type": "object",
            "required": ["first_name", "last_name", "email", "password"],
            "properties": {
                "first_name": {"type": "string", "example": "Maya"},
                "last_name": {"type": "string", "example": "Wrench"},
                "email": {"type": "string", "example": "maya@example.com"},
                "password": {"type": "string", "example": "password123"},
                "phone": {"type": "string", "example": "555-0111"},
                "specialty": {"type": "string", "example": "Diagnostics"},
            },
        },
        "MechanicUpdatePayload": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string", "example": "Maya"},
                "last_name": {"type": "string", "example": "Updated"},
                "email": {"type": "string", "example": "maya.updated@example.com"},
                "password": {"type": "string", "example": "newpass123"},
                "phone": {"type": "string", "example": "555-0122"},
                "specialty": {"type": "string", "example": "Electrical"},
            },
        },
        "MechanicResponse": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "first_name": {"type": "string", "example": "Maya"},
                "last_name": {"type": "string", "example": "Wrench"},
                "email": {"type": "string", "example": "maya@example.com"},
                "phone": {"type": "string", "example": "555-0111"},
                "specialty": {"type": "string", "example": "Diagnostics"},
            },
        },
        "InventoryPayload": {
            "type": "object",
            "required": ["name", "price"],
            "properties": {
                "name": {"type": "string", "example": "Oil Filter"},
                "price": {"type": "number", "format": "float", "example": 12.99},
            },
        },
        "InventoryResponse": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Oil Filter"},
                "price": {"type": "number", "format": "float", "example": 12.99},
            },
        },
        "ServiceTicketPayload": {
            "type": "object",
            "required": ["customer_id", "vin", "description"],
            "properties": {
                "customer_id": {"type": "integer", "example": 1},
                "vin": {"type": "string", "example": "1HGCM82633A004352"},
                "description": {
                    "type": "string",
                    "example": "Oil change and brake inspection",
                },
                "service_date": {"type": "string", "example": "2026-08-01"},
                "status": {"type": "string", "example": "open"},
                "mechanic_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "example": [1],
                },
                "part_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "example": [1],
                },
            },
        },
        "ServiceTicketUpdatePayload": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "integer", "example": 1},
                "vin": {"type": "string", "example": "1HGCM82633A004352"},
                "description": {"type": "string", "example": "Updated repair notes"},
                "service_date": {"type": "string", "example": "2026-08-02"},
                "status": {"type": "string", "example": "in progress"},
            },
        },
        "ServiceTicketResponse": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "customer_id": {"type": "integer", "example": 1},
                "vin": {"type": "string", "example": "1HGCM82633A004352"},
                "description": {
                    "type": "string",
                    "example": "Oil change and brake inspection",
                },
                "status": {"type": "string", "example": "open"},
                "mechanics": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/MechanicResponse"},
                },
                "parts": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/InventoryResponse"},
                },
            },
        },
        "MessageResponse": {
            "type": "object",
            "properties": {"message": {"type": "string", "example": "Deleted"}},
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {"error": {"type": "string", "example": "Not found"}},
        },
    }


def paths():
    return {
        "/": {
            "get": {
                "tags": ["Root"],
                "summary": "API landing route",
                "description": "Returns a list of available API resources.",
                "responses": {
                    "200": response(
                        "API metadata",
                        example={
                            "message": "Backend Documentation and Testing API",
                            "resources": {
                                "customers": "/customers",
                                "mechanics": "/mechanics",
                            },
                        },
                    )
                },
            }
        },
        "/customers/": {
            "post": {
                "tags": ["Customers"],
                "summary": "Create customer",
                "description": "Creates a new customer account with a hashed password.",
                "parameters": body_parameter("CustomerPayload"),
                "responses": {
                    "201": response("Created customer", "CustomerResponse"),
                    "409": response("Duplicate email", "ErrorResponse"),
                },
            },
            "get": {
                "tags": ["Customers"],
                "summary": "Get customers",
                "description": "Retrieves all customers.",
                "responses": {
                    "200": {
                        "description": "Customer list",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/CustomerResponse"},
                        },
                    }
                },
            },
        },
        "/customers/login": {
            "post": {
                "tags": ["Customers"],
                "summary": "Customer login",
                "description": "Validates a customer email and password and returns a bearer token.",
                "parameters": body_parameter("LoginPayload"),
                "responses": {
                    "200": response("Customer login token", "LoginResponse"),
                    "401": response("Invalid credentials", "ErrorResponse"),
                },
            }
        },
        "/customers/my-tickets": {
            "get": {
                "tags": ["Customers"],
                "summary": "Get current customer's tickets",
                "description": "Uses the customer bearer token to retrieve only that customer's service tickets.",
                "security": bearer_security(),
                "responses": {
                    "200": {
                        "description": "Customer service tickets",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                    },
                    "401": response("Missing or invalid token", "ErrorResponse"),
                },
            }
        },
        "/customers/{customer_id}": resource_by_id_paths(
            "Customers",
            "customer_id",
            "Customer ID",
            "CustomerUpdatePayload",
            "CustomerResponse",
            protected=True,
        ),
        "/mechanics/": {
            "post": {
                "tags": ["Mechanics"],
                "summary": "Create mechanic",
                "description": "Creates a new mechanic account with a hashed password.",
                "parameters": body_parameter("MechanicPayload"),
                "responses": {
                    "201": response("Created mechanic", "MechanicResponse"),
                    "409": response("Duplicate email", "ErrorResponse"),
                },
            },
            "get": {
                "tags": ["Mechanics"],
                "summary": "Get mechanics",
                "description": "Retrieves all mechanics.",
                "responses": {
                    "200": {
                        "description": "Mechanic list",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/MechanicResponse"},
                        },
                    }
                },
            },
        },
        "/mechanics/login": {
            "post": {
                "tags": ["Mechanics"],
                "summary": "Mechanic login",
                "description": "Validates mechanic credentials and returns a mechanic bearer token.",
                "parameters": body_parameter("LoginPayload"),
                "responses": {
                    "200": response("Mechanic login token", "LoginResponse"),
                    "401": response("Invalid credentials", "ErrorResponse"),
                },
            }
        },
        "/mechanics/{mechanic_id}": resource_by_id_paths(
            "Mechanics",
            "mechanic_id",
            "Mechanic ID",
            "MechanicUpdatePayload",
            "MechanicResponse",
            protected=True,
        ),
        "/inventory/": {
            "post": {
                "tags": ["Inventory"],
                "summary": "Create inventory item",
                "description": "Creates a new part in inventory. Requires mechanic authorization.",
                "security": bearer_security(),
                "parameters": body_parameter("InventoryPayload"),
                "responses": {
                    "201": response("Created inventory item", "InventoryResponse"),
                    "401": response("Missing token", "ErrorResponse"),
                },
            },
            "get": {
                "tags": ["Inventory"],
                "summary": "Get inventory",
                "description": "Retrieves all inventory parts.",
                "responses": {
                    "200": {
                        "description": "Inventory list",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/InventoryResponse"},
                        },
                    }
                },
            },
        },
        "/inventory/{part_id}": resource_by_id_paths(
            "Inventory",
            "part_id",
            "Part ID",
            "InventoryPayload",
            "InventoryResponse",
            protected=True,
        ),
        "/service-tickets/": {
            "post": {
                "tags": ["Service Tickets"],
                "summary": "Create service ticket",
                "description": "Creates a service ticket for a customer. Requires mechanic authorization.",
                "security": bearer_security(),
                "parameters": body_parameter("ServiceTicketPayload"),
                "responses": {
                    "201": response("Created service ticket", "ServiceTicketResponse"),
                    "404": response("Customer, mechanic, or part not found", "ErrorResponse"),
                },
            },
            "get": {
                "tags": ["Service Tickets"],
                "summary": "Get service tickets",
                "description": "Retrieves all service tickets.",
                "responses": {
                    "200": {
                        "description": "Service ticket list",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/ServiceTicketResponse"},
                        },
                    }
                },
            },
        },
        "/service-tickets/{ticket_id}": resource_by_id_paths(
            "Service Tickets",
            "ticket_id",
            "Service ticket ID",
            "ServiceTicketUpdatePayload",
            "ServiceTicketResponse",
            protected=True,
        ),
        "/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}": relation_path(
            "Assigns a mechanic to a service ticket."
        ),
        "/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}": relation_path(
            "Removes a mechanic from a service ticket."
        ),
        "/service-tickets/{ticket_id}/add-part/{part_id}": {
            "put": {
                "tags": ["Service Tickets"],
                "summary": "Add part to ticket",
                "description": "Adds an inventory part to a service ticket. Requires mechanic authorization.",
                "security": bearer_security(),
                "parameters": [
                    id_parameter("ticket_id", "Service ticket ID"),
                    id_parameter("part_id", "Inventory part ID"),
                ],
                "responses": {
                    "200": response("Updated service ticket", "ServiceTicketResponse"),
                    "404": response("Service ticket or part not found", "ErrorResponse"),
                },
            }
        },
    }


def resource_by_id_paths(tag, parameter_name, parameter_description, payload, response_def, protected):
    security = bearer_security() if protected else None
    path_parameters = [id_parameter(parameter_name, parameter_description)]
    update_parameters = path_parameters + body_parameter(payload)
    data = {
        "get": {
            "tags": [tag],
            "summary": f"Get {tag[:-1].lower()} by ID",
            "description": f"Retrieves one {tag[:-1].lower()} by ID.",
            "parameters": path_parameters,
            "responses": {
                "200": response(f"{tag[:-1]} data", response_def),
                "404": response("Not found", "ErrorResponse"),
            },
        },
        "put": {
            "tags": [tag],
            "summary": f"Update {tag[:-1].lower()}",
            "description": f"Updates one {tag[:-1].lower()} by ID.",
            "parameters": update_parameters,
            "responses": {
                "200": response(f"Updated {tag[:-1].lower()}", response_def),
                "401": response("Missing token", "ErrorResponse"),
                "404": response("Not found", "ErrorResponse"),
            },
        },
        "delete": {
            "tags": [tag],
            "summary": f"Delete {tag[:-1].lower()}",
            "description": f"Deletes one {tag[:-1].lower()} by ID.",
            "parameters": path_parameters,
            "responses": {
                "200": response("Delete confirmation", "MessageResponse"),
                "401": response("Missing token", "ErrorResponse"),
                "404": response("Not found", "ErrorResponse"),
            },
        },
    }

    if security:
        data["put"]["security"] = security
        data["delete"]["security"] = security

    return data


def relation_path(description):
    return {
        "put": {
            "tags": ["Service Tickets"],
            "summary": "Update ticket mechanic relationship",
            "description": description + " Requires mechanic authorization.",
            "security": bearer_security(),
            "parameters": [
                id_parameter("ticket_id", "Service ticket ID"),
                id_parameter("mechanic_id", "Mechanic ID"),
            ],
            "responses": {
                "200": response("Updated service ticket", "ServiceTicketResponse"),
                "400": response("Invalid relationship change", "ErrorResponse"),
                "404": response("Service ticket or mechanic not found", "ErrorResponse"),
            },
        }
    }
