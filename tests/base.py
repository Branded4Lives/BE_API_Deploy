import unittest

from app import create_app
from app.extensions import db


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SECRET_KEY = "test-secret"


class BaseAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def create_customer(self, email="customer@example.com"):
        response = self.client.post(
            "/customers/",
            json={
                "first_name": "Brandon",
                "last_name": "Customer",
                "email": email,
                "password": "password123",
                "phone": "555-0100",
                "address": "123 Main St",
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def login_customer(self, email="customer@example.com"):
        response = self.client.post(
            "/customers/login",
            json={"email": email, "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def customer_headers(self, email="customer@example.com"):
        token = self.login_customer(email)
        return {"Authorization": f"Bearer {token}"}

    def create_mechanic(self, email="mechanic@example.com"):
        response = self.client.post(
            "/mechanics/",
            json={
                "first_name": "Maya",
                "last_name": "Wrench",
                "email": email,
                "password": "password123",
                "phone": "555-0111",
                "specialty": "Diagnostics",
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def login_mechanic(self, email="mechanic@example.com"):
        response = self.client.post(
            "/mechanics/login",
            json={"email": email, "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        return response.get_json()["token"]

    def mechanic_headers(self, email="mechanic@example.com"):
        token = self.login_mechanic(email)
        return {"Authorization": f"Bearer {token}"}

    def create_inventory_item(self, headers=None, name="Oil Filter"):
        if headers is None:
            headers = self.mechanic_headers()

        response = self.client.post(
            "/inventory/",
            headers=headers,
            json={"name": name, "price": 12.99},
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_service_ticket(self, headers=None, customer_id=None, mechanic_ids=None, part_ids=None):
        if headers is None:
            headers = self.mechanic_headers()
        if customer_id is None:
            customer_id = self.create_customer()["id"]
        if mechanic_ids is None:
            mechanic_ids = []
        if part_ids is None:
            part_ids = []

        response = self.client.post(
            "/service-tickets/",
            headers=headers,
            json={
                "customer_id": customer_id,
                "vin": "1HGCM82633A004352",
                "description": "Oil change and brake inspection",
                "service_date": "2026-08-01",
                "status": "open",
                "mechanic_ids": mechanic_ids,
                "part_ids": part_ids,
            },
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()
