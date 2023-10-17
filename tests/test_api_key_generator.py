import unittest
from unittest.mock import patch
from api.api_key_generation import APIKeyGeneratorService  # Update this import
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if it exists


class TestAPIKeyGeneratorService(unittest.TestCase):
    admin_email = os.getenv(
        "ADMIN_EMAIL", "admin@example.com"
    )  # Fetch admin email from env variables or default to 'admin@example.com'
    admin_api_key = os.getenv(
        "ADMIN_API_KEY", "AdminAPIkey"
    )  # Fetch admin api key from env variables or default to 'AdminAPIkey'

    @patch("api.api_key_generation.requests.post")  # Update this import
    def test_generate_api_key_successful(self, mock_post):
        mock_response = {
            "vendor_email": "vendor@example.com",
            "api_key": "e7297267e13cbfa8ac691367c6fc3d96",
        }
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        generator = APIKeyGeneratorService(self.admin_email, self.admin_api_key)
        response = generator.generate_api_key("vendor2@example.com")
        print(f"Response: {response}")  # Print the response

        self.assertEqual(response, mock_response)

    @patch("api.api_key_generation.requests.post")  # Update this import
    def test_generate_api_key_failed(self, mock_post):
        mock_post.return_value.status_code = 400

        generator = APIKeyGeneratorService(self.admin_email, self.admin_api_key)

        with self.assertRaises(ConnectionError):
            generator.generate_api_key("vendor@example.com")

    @patch("api.api_key_generation.requests.post")  # Update this import
    def test_generate_api_key_invalid_json(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.side_effect = json.JSONDecodeError(
            "Invalid JSON", "", 0
        )

        generator = APIKeyGeneratorService(self.admin_email, self.admin_api_key)

        with self.assertRaises(ValueError):
            generator.generate_api_key("vendor@example.com")


if __name__ == "__main__":
    unittest.main()
