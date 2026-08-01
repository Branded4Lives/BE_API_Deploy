from tests.base import BaseAPITestCase


class MechanicRouteTests(BaseAPITestCase):
    def test_create_mechanic(self):
        mechanic = self.create_mechanic()

        self.assertEqual(mechanic["email"], "mechanic@example.com")

    def test_create_mechanic_duplicate_email_negative(self):
        self.create_mechanic()
        response = self.client.post(
            "/mechanics/",
            json={
                "first_name": "Second",
                "last_name": "Mechanic",
                "email": "mechanic@example.com",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_login_mechanic(self):
        self.create_mechanic()
        response = self.client.post(
            "/mechanics/login",
            json={"email": "mechanic@example.com", "password": "password123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_mechanic_invalid_password_negative(self):
        self.create_mechanic()
        response = self.client.post(
            "/mechanics/login",
            json={"email": "mechanic@example.com", "password": "bad-password"},
        )

        self.assertEqual(response.status_code, 401)

    def test_get_mechanics(self):
        self.create_mechanic()
        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_mechanic_by_id(self):
        mechanic = self.create_mechanic()
        response = self.client.get(f"/mechanics/{mechanic['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], mechanic["id"])

    def test_get_mechanic_not_found_negative(self):
        response = self.client.get("/mechanics/999")

        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_requires_token_negative(self):
        mechanic = self.create_mechanic()
        response = self.client.put(
            f"/mechanics/{mechanic['id']}",
            json={"specialty": "Electrical"},
        )

        self.assertEqual(response.status_code, 401)

    def test_update_mechanic(self):
        mechanic = self.create_mechanic()
        headers = self.mechanic_headers()
        response = self.client.put(
            f"/mechanics/{mechanic['id']}",
            headers=headers,
            json={"specialty": "Electrical"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["specialty"], "Electrical")

    def test_delete_mechanic(self):
        mechanic = self.create_mechanic()
        headers = self.mechanic_headers()
        response = self.client.delete(f"/mechanics/{mechanic['id']}", headers=headers)

        self.assertEqual(response.status_code, 200)
