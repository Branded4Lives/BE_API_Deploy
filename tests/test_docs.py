from tests.base import BaseAPITestCase


class DocsRouteTests(BaseAPITestCase):
    def test_root_route(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Mechanic Shop API Deployment")

    def test_swagger_json_route(self):
        response = self.client.get("/swagger.json")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("/customers/", data["paths"])
        self.assertIn("CustomerPayload", data["definitions"])
        self.assertIn("Bearer", data["securityDefinitions"])

    def test_swagger_ui_route(self):
        response = self.client.get("/docs/")

        self.assertEqual(response.status_code, 200)
