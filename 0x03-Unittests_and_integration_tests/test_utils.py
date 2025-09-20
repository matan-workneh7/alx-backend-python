#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json 


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    # Valid path tests
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # Exception tests
    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # str(context.exception) includes quotes, so expected_key must include quotes
        self.assertEqual(str(context.exception), expected_key)

class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test get_json returns expected payload and calls requests.get correctly."""

        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for url, payload in test_cases:
            fake_response = Mock()
            fake_response.json.return_value = payload
            mock_get.return_value = fake_response
            result = get_json(url)
            mock_get.assert_called_with(url)
            self.assertEqual(result, payload)

if __name__ == "__main__":
    unittest.main()
