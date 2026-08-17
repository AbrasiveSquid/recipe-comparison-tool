import socket
import unittest
from unittest.mock import Mock, call, patch

from recipe_logic.recipe_scraper import (
    MAX_REDIRECTS,
    _get_with_safe_redirects,
    validate_public_url,
)

from recipe_logic.recipe_scraper import validate_public_url


class TestValidatePublicUrl(unittest.TestCase):
    def test_rejects_invalid_url_formats(self):
        invalid_urls = (
            "",
            "not-a-url",
            "ftp://example.com/recipe",
            "http:///missing-host",
            "https://user:password@example.com/recipe",
            "https://example.com:8080/recipe",
        )

        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_public_url(url)

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            validate_public_url(None)

    @patch("recipe_logic.recipe_scraper.socket.getaddrinfo")
    def test_accepts_public_address(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("93.184.216.34", 443),
            )
        ]

        self.assertTrue(
            validate_public_url("https://example.com/recipe")
        )

    @patch("recipe_logic.recipe_scraper.socket.getaddrinfo")
    def test_rejects_non_public_addresses(self, mock_getaddrinfo):
        for address in (
            "127.0.0.1",
            "10.0.0.1",
            "169.254.169.254",
            "::1",
        ):
            with self.subTest(address=address):
                mock_getaddrinfo.return_value = [
                    (
                        socket.AF_INET,
                        socket.SOCK_STREAM,
                        socket.IPPROTO_TCP,
                        "",
                        (address, 443),
                    )
                ]

                with self.assertRaises(ValueError):
                    validate_public_url("https://example.com/recipe")

    @patch("recipe_logic.recipe_scraper.socket.getaddrinfo")
    def test_rejects_hostname_with_mixed_addresses(
        self,
        mock_getaddrinfo,
    ):
        mock_getaddrinfo.return_value = [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("93.184.216.34", 443),
            ),
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("10.0.0.1", 443),
            ),
        ]

        with self.assertRaises(ValueError):
            validate_public_url("https://example.com/recipe")


class TestSafeRedirects(unittest.TestCase):
    @patch("recipe_logic.recipe_scraper.validate_public_url")
    def test_follows_validated_redirect(self, mock_validate):
        redirect_response = Mock(
            status_code=302,
            headers={"Location": "/recipe"},
        )
        final_response = Mock(status_code=200, headers={})
        request_get = Mock(
            side_effect=[redirect_response, final_response]
        )

        result = _get_with_safe_redirects(
            request_get,
            "https://example.com/start",
            timeout=15,
        )

        self.assertIs(result, final_response)
        self.assertEqual(
            mock_validate.call_args_list,
            [
                call("https://example.com/start"),
                call("https://example.com/recipe"),
            ],
        )
        self.assertEqual(
            request_get.call_args_list,
            [
                call(
                    "https://example.com/start",
                    allow_redirects=False,
                    timeout=15,
                ),
                call(
                    "https://example.com/recipe",
                    allow_redirects=False,
                    timeout=15,
                ),
            ],
        )
        redirect_response.close.assert_called_once()

    @patch("recipe_logic.recipe_scraper.validate_public_url")
    def test_blocks_unsafe_redirect_before_request(
        self,
        mock_validate,
    ):
        mock_validate.side_effect = [
            True,
            ValueError("URL resolves to a non-public address"),
        ]
        redirect_response = Mock(
            status_code=302,
            headers={"Location": "http://127.0.0.1"},
        )
        request_get = Mock(return_value=redirect_response)

        with self.assertRaises(ValueError):
            _get_with_safe_redirects(
                request_get,
                "https://example.com/start",
            )

        request_get.assert_called_once_with(
            "https://example.com/start",
            allow_redirects=False,
        )

    @patch("recipe_logic.recipe_scraper.validate_public_url")
    def test_enforces_redirect_limit(self, mock_validate):
        responses = [
            Mock(
                status_code=302,
                headers={"Location": f"/redirect-{number}"},
            )
            for number in range(MAX_REDIRECTS + 1)
        ]
        request_get = Mock(side_effect=responses)

        with self.assertRaisesRegex(
            ValueError,
            "redirect limit",
        ):
            _get_with_safe_redirects(
                request_get,
                "https://example.com/start",
            )

        self.assertEqual(request_get.call_count, MAX_REDIRECTS + 1)