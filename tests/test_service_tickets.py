from tests.base import BaseAPITestCase


class ServiceTicketRouteTests(BaseAPITestCase):
    def test_create_service_ticket_requires_token_negative(self):
        customer = self.create_customer()
        response = self.client.post(
            "/service-tickets/",
            json={
                "customer_id": customer["id"],
                "vin": "1HGCM82633A004352",
                "description": "Oil change",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_create_service_ticket(self):
        customer = self.create_customer()
        self.create_mechanic()
        ticket = self.create_service_ticket(customer_id=customer["id"])

        self.assertEqual(ticket["customer_id"], customer["id"])

    def test_create_service_ticket_missing_customer_negative(self):
        self.create_mechanic()
        response = self.client.post(
            "/service-tickets/",
            headers=self.mechanic_headers(),
            json={
                "customer_id": 999,
                "vin": "1HGCM82633A004352",
                "description": "Oil change",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_service_tickets(self):
        customer = self.create_customer()
        self.create_mechanic()
        self.create_service_ticket(customer_id=customer["id"])
        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_service_ticket_by_id(self):
        customer = self.create_customer()
        self.create_mechanic()
        ticket = self.create_service_ticket(customer_id=customer["id"])
        response = self.client.get(f"/service-tickets/{ticket['id']}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], ticket["id"])

    def test_get_service_ticket_not_found_negative(self):
        response = self.client.get("/service-tickets/999")

        self.assertEqual(response.status_code, 404)

    def test_update_service_ticket(self):
        customer = self.create_customer()
        self.create_mechanic()
        headers = self.mechanic_headers()
        ticket = self.create_service_ticket(headers=headers, customer_id=customer["id"])
        response = self.client.put(
            f"/service-tickets/{ticket['id']}",
            headers=headers,
            json={"status": "in progress"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "in progress")

    def test_assign_mechanic_to_service_ticket(self):
        customer = self.create_customer()
        mechanic = self.create_mechanic()
        headers = self.mechanic_headers()
        ticket = self.create_service_ticket(headers=headers, customer_id=customer["id"])
        response = self.client.put(
            f"/service-tickets/{ticket['id']}/assign-mechanic/{mechanic['id']}",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["mechanics"]), 1)

    def test_remove_mechanic_from_service_ticket(self):
        customer = self.create_customer()
        mechanic = self.create_mechanic()
        headers = self.mechanic_headers()
        ticket = self.create_service_ticket(
            headers=headers,
            customer_id=customer["id"],
            mechanic_ids=[mechanic["id"]],
        )
        response = self.client.put(
            f"/service-tickets/{ticket['id']}/remove-mechanic/{mechanic['id']}",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["mechanics"]), 0)

    def test_remove_unassigned_mechanic_negative(self):
        customer = self.create_customer()
        mechanic = self.create_mechanic()
        headers = self.mechanic_headers()
        ticket = self.create_service_ticket(headers=headers, customer_id=customer["id"])
        response = self.client.put(
            f"/service-tickets/{ticket['id']}/remove-mechanic/{mechanic['id']}",
            headers=headers,
        )

        self.assertEqual(response.status_code, 400)

    def test_add_part_to_service_ticket(self):
        customer = self.create_customer()
        self.create_mechanic()
        headers = self.mechanic_headers()
        part = self.create_inventory_item(headers=headers)
        ticket = self.create_service_ticket(headers=headers, customer_id=customer["id"])
        response = self.client.put(
            f"/service-tickets/{ticket['id']}/add-part/{part['id']}",
            headers=headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["parts"]), 1)

    def test_delete_service_ticket(self):
        customer = self.create_customer()
        self.create_mechanic()
        headers = self.mechanic_headers()
        ticket = self.create_service_ticket(headers=headers, customer_id=customer["id"])
        response = self.client.delete(f"/service-tickets/{ticket['id']}", headers=headers)

        self.assertEqual(response.status_code, 200)
