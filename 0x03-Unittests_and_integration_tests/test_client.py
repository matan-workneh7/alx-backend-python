#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

try:
    from .fixtures import org_payload, repos_payload, expected_repos, apache2_repos
except ImportError:
    from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value."""
        fake_payload = {"org": org_name}
        mock_get_json.return_value = fake_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, fake_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property returns correct URL."""
        client = GithubOrgClient("abc")
        with patch.object(
            GithubOrgClient, "org", return_value={"repos_url": "http://repos"}
        ):
            self.assertEqual(client._public_repos_url, "http://repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names."""
        mock_get_json.return_value = [
            {"name": "repo1"}, {"name": "repo2"}
        ]
        client = GithubOrgClient("abc")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://repos"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        client = GithubOrgClient("abc")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures and patch requests.get."""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse(cls.org_payload)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns filtered repos by license."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )


class MockResponse:
    """Mock response object for requests.get()."""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

if __name__ == "__main__":
    unittest.main()