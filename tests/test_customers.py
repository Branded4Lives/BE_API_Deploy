from tests.base import BaseAPITestCase


class CustomerRouteTests(BaseAPITestCase):
    def test_create_customer(self):
        customer = self.create_customer()

        self.assertEqual(customer["email"], "customer@example.com")
        self.assertNotIn("password_hash", customer)

    def test_create_customer_duplicate_email_negative(self):
        self.create_customer()
        response = self.client.post(
            "/customers/",
            json={
                "first_name": "Second",
                "last_name": "Customer",
                "email": "customer@example.com",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_login_customer(self):
        self.create_customer()
        response = self.client.post(
            "/customers/login",
            json={"email": "customer@example.com", "password": "password123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_customer_invalid_password_negative(self):
        self.create_customer()
        response = self.client.post(
            "/customers/login",
            json={"email": "customer@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)

    def test_get_customers(self):
        self.create_customer()
        response = self.client.get("/customers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_customer_by_id(self):
        customer = self.create_customer()
        response = self.client.get(f"/customers/{customer['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], customer["id"])

    def test_get_customer_not_found_negative(self):
        response = self.client.get("/customers/999")

        self.assertEqual(response.status_code, 404)

    def test_update_customer_requires_token_negative(self):
        customer = self.create_customer()
        response = self.client.put(
            f"/customers/{customer['id']}",
            json={"phone": "555-9999"},
        )

        self.assertEqual(response.status_code, 401)

    def test_update_customer(self):
        customer = self.create_customer()
        headers = self.customer_headers()
        response = self.client.put(
            f"/customers/{customer['id']}",
            headers=headers,
            json={"phone": "555-9999"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["phone"], "555-9999")

    def test_get_my_tickets(self):
        customer = self.create_customer()
        self.create_mechanic()
        mechanic_headers = self.mechanic_headers()
        self.create_service_ticket(headers=mechanic_headers, customer_id=customer["id"])
        customer_headers = self.customer_headers()
        response = self.client.get("/customers/my-tickets", headers=customer_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_delete_customer(self):
        customer = self.create_customer()
        headers = self.customer_headers()
        response = self.client.delete(f"/customers/{customer['id']}", headers=headers)

        self.assertEqual(response.status_code, 200)
