import io
import unittest
from unittest.mock import patch

from app import app


class TestOcrRoute(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_rejects_missing_image(self):
        response = self.client.post("/ocr")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "No image provided"},
        )

    @patch("app.routes.extract_text")
    def test_returns_extracted_text(self, mock_extract_text):
        mock_extract_text.return_value = "1 cup flour\n2 eggs"

        response = self.client.post(
            "/ocr",
            data={
                "image": (
                    io.BytesIO(b"fake image data"),
                    "recipe.png",
                )
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"text": "1 cup flour\n2 eggs"},
        )
        mock_extract_text.assert_called_once()

    @patch("app.routes.extract_text")
    def test_handles_ocr_failure(self, mock_extract_text):
        mock_extract_text.side_effect = Exception("Azure failed")

        response = self.client.post(
            "/ocr",
            data={
                "image": (
                    io.BytesIO(b"fake image data"),
                    "recipe.png",
                )
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.get_json(),
            {"error": "Could not extract text from image"},
        )

    def test_rejects_image_over_10_mb(self):
        response = self.client.post(
            "/ocr",
            data={
                "image": (
                    io.BytesIO(b"x" * (10 * 1024 * 1024 + 1)),
                    "recipe.png",
                )
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(
            response.get_json(),
            {"error": "Image must be 10 MB or smaller"},
        )
    @patch("app.routes.extract_text")
    def test_rate_limits_ocr_requests(self, mock_extract_text):
        mock_extract_text.return_value = "1 cup flour"

        headers = {"X-Forwarded-For": "203.0.113.10"}

        for _ in range(5):
            response = self.client.post(
                "/ocr",
                data={
                    "image": (
                        io.BytesIO(b"fake image"),
                        "recipe.png",
                    )
                },
                content_type="multipart/form-data",
                headers=headers,
            )

            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/ocr",
            data={
                "image": (
                    io.BytesIO(b"fake image"),
                    "recipe.png",
                )
            },
            content_type="multipart/form-data",
            headers=headers,
        )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.get_json(),
            {"error": "Too many image requests. Please try again later."},
        )
