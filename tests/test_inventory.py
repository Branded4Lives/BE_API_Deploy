from tests.base import BaseAPITestCase


class InventoryRouteTests(BaseAPITestCase):
    def test_create_inventory_requires_token_negative(self):
        response = self.client.post(
            "/inventory/",
            json={"name": "Oil Filter", "price": 12.99},
        )

        self.assertEqual(response.status_code, 401)

    def test_create_inventory_item(self):
        self.create_mechanic()
        item = self.create_inventory_item()

        self.assertEqual(item["name"], "Oil Filter")

    def test_create_inventory_duplicate_name_negative(self):
        self.create_mechanic()
        self.create_inventory_item()
        response = self.client.post(
            "/inventory/",
            headers=self.mechanic_headers(),
            json={"name": "Oil Filter", "price": 15.99},
        )

        self.assertEqual(response.status_code, 409)

    def test_get_inventory_items(self):
        self.create_mechanic()
        self.create_inventory_item()
        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_inventory_item_by_id(self):
        self.create_mechanic()
        item = self.create_inventory_item()
        response = self.client.get(f"/inventory/{item['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], item["id"])

    def test_get_inventory_item_not_found_negative(self):
        response = self.client.get("/inventory/999")

        self.assertEqual(response.status_code, 404)

    def test_update_inventory_item(self):
        self.create_mechanic()
        headers = self.mechanic_headers()
        item = self.create_inventory_item(headers=headers)
        response = self.client.put(
            f"/inventory/{item['id']}",
            headers=headers,
            json={"price": 14.99},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["price"], 14.99)

    def test_delete_inventory_item(self):
        self.create_mechanic()
        headers = self.mechanic_headers()
        item = self.create_inventory_item(headers=headers)
        response = self.client.delete(f"/inventory/{item['id']}", headers=headers)

        self.assertEqual(response.status_code, 200)
