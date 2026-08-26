import unittest
from unittest.mock import patch

from app import app, limiter


class TestFeedbackRoute(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        limiter.reset()

    @patch("app.routes.send_feedback")
    def test_sends_feedback(self, mock_send_feedback):
        response = self.client.post(
            "/feedback",
            json={"message": "This is useful."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Feedback sent"})
        mock_send_feedback.assert_called_once_with("This is useful.")

    @patch("app.routes.send_feedback")
    def test_rejects_empty_feedback(self, mock_send_feedback):
        response = self.client.post(
            "/feedback",
            json={"message": "   "},
        )

        self.assertEqual(response.status_code, 400)
        mock_send_feedback.assert_not_called()

    @patch("app.routes.send_feedback")
    def test_rejects_feedback_over_2000_characters(self, mock_send_feedback):
        response = self.client.post(
            "/feedback",
            json={"message": "a" * 2001},
        )

        self.assertEqual(response.status_code, 400)
        mock_send_feedback.assert_not_called()

    @patch("app.routes.send_feedback")
    def test_handles_email_failure(self, mock_send_feedback):
        mock_send_feedback.side_effect = Exception("Resend failed")

        response = self.client.post(
            "/feedback",
            json={"message": "Something broke."},
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.get_json(),
            {"error": "Could not send feedback"},
        )


if __name__ == "__main__":
    unittest.main()
