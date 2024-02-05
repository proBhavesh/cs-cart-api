import unittest
import json
from unittest.mock import MagicMock, patch
from api import BASE_URL, encode_credentials
from api.orders import OrdersService

class TestOrdersService(unittest.TestCase):

    def setUp(self):
        self.email = "test@example.com"
        self.api_key = "abcdefg123456"
        self.orders_service = OrdersService(email=self.email, api_key=self.api_key)

    def test_get_orders(self):
        response_data = [{"order_id": 1, "status": "pending"}, {"order_id": 2, "status": "completed"}]
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = response_data
            orders = self.orders_service.get_orders()
            self.assertIsInstance(orders, list)
            self.assertEqual(len(orders), 2)
            self.assertIsInstance(orders[0], dict)
            self.assertTrue("order_id" in orders[0])
            self.assertTrue("status" in orders[0])

    def test_get_order(self):
        order_id = 1
        response_data = {"order_id": order_id, "status": "pending", "total_price": 10.99}
        with patch("requests.get") as mock_get:
            url = self.orders_service.url + str(order_id)
            mock_get.return_value.json.return_value = response_data
            order = self.orders_service.get_order(order_id=order_id)
            self.assertIsInstance(order, dict)
            self.assertTrue("order_id" in order)
            self.assertEqual(order["order_id"], order_id)
            self.assertTrue("status" in order)
            self.assertEqual(order["status"], "pending")

    def test_create_order(self):
        new_order = {"item": "product", "quantity": 2, "price": 15.99}
        response_data = {"order_id": 3, "status": "created"}
        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = response_data
            order = self.orders_service.create_order(new_order)
            self.assertIsInstance(order, dict)
            self.assertTrue("order_id" in order)
            self.assertEqual(order["order_id"], 3)
            self.assertTrue("status" in order)
            self.assertEqual(order["status"], "created")

    # TODO: 
    def test_update_order(self):
        order_id = 1
        new_order = {"status": "processing"}
        with patch("requests.put") as mock_put:
            url = self.orders_service.url + str(order_id)
            mock_put.return_value.json.return_value = {"status": "processing"}
            self.orders_service.update_order(order_id=order_id, order_data=new_order)
            order = self.orders_service.get_order(order_id=order_id)
            self.assertIsInstance(order, dict)
            self.assertEqual(order["status"], "processing")

    # TODO: Fix Return Type
    def test_delete_order(self):
        order_id = 1
        with patch("requests.delete") as mock_delete:
            url = self.orders_service.url + str(order_id)
            mock_delete.return_value.status_code = 204
            result = self.orders_service.delete_order(order_id=order_id)
            print(result)
            self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()
